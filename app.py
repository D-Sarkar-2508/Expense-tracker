from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from sqlalchemy import func
import calendar
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'error'

# ---------- MODELS ----------

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    expenses = db.relationship('Expense', backref='owner', lazy=True)

class Expense(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(100), nullable=False)
    amount   = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date     = db.Column(db.Date, nullable=False, default=date.today)
    note     = db.Column(db.String(200), nullable=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Expense {self.title} ₹{self.amount}>'

CATEGORIES = ['Food', 'Transport', 'Shopping', 'Health', 'Entertainment', 'Bills', 'Education', 'Other']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- AUTH ROUTES ----------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        user = User(username=username, email=email,
                    password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


# ---------- EXPENSE ROUTES ----------

@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    cat_totals = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter_by(user_id=current_user.id)
        .group_by(Expense.category)
        .all()
    )
    cat_labels = [c[0] for c in cat_totals]
    cat_values = [round(c[1], 2) for c in cat_totals]
    return render_template('index.html', expenses=expenses, total=round(total, 2),
                           categories=CATEGORIES, cat_labels=cat_labels, cat_values=cat_values)


@app.route('/add', methods=['POST'])
@login_required
def add_expense():
    title    = request.form.get('title', '').strip()
    amount   = request.form.get('amount', '')
    category = request.form.get('category', '')
    date_str = request.form.get('date', '')
    note     = request.form.get('note', '').strip()

    if not title or not amount or not category or not date_str:
        flash('Please fill all required fields.', 'error')
        return redirect(url_for('index'))
    try:
        amount = float(amount)
        if amount <= 0: raise ValueError
    except ValueError:
        flash('Amount must be a positive number.', 'error')
        return redirect(url_for('index'))
    try:
        expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format.', 'error')
        return redirect(url_for('index'))

    expense = Expense(title=title, amount=amount, category=category,
                      date=expense_date, note=note, user_id=current_user.id)
    db.session.add(expense)
    db.session.commit()
    flash('Expense added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        expense.title    = request.form.get('title', '').strip()
        expense.category = request.form.get('category', '')
        expense.note     = request.form.get('note', '').strip()
        try:
            expense.amount = float(request.form.get('amount', 0))
            expense.date   = datetime.strptime(request.form.get('date', ''), '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid amount or date.', 'error')
            return redirect(url_for('edit_expense', id=id))
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', expense=expense, categories=CATEGORIES)


@app.route('/monthly')
@login_required
def monthly():
    selected_year = request.args.get('year', str(datetime.now().year))
    all_years = db.session.query(
        func.to_char(Expense.date, 'YYYY').label('year')
    ).filter_by(user_id=current_user.id).group_by('year').order_by('year').all()
    available_years = [int(r.year) for r in all_years]

    results = (
        db.session.query(
            func.to_char(Expense.date, 'YYYY').label('year'),
            func.to_char(Expense.date, 'MM').label('month'),
            func.sum(Expense.amount).label('total')
        )
        .filter(Expense.user_id == current_user.id,
                func.to_char(Expense.date, 'YYYY') == selected_year)
        .group_by('year', 'month').order_by('month').all()
    )
    monthly_data = []
    for r in results:
        monthly_data.append({
            'label': f"{calendar.month_abbr[int(r.month)]} {r.year}",
            'total': round(r.total, 2),
            'year': int(r.year),
            'month': int(r.month)
        })
    return render_template('monthly.html', monthly_data=monthly_data,
                           selected_year=int(selected_year),
                           available_years=available_years)


@app.route('/monthly/<int:year>/<int:month>')
@login_required
def monthly_detail(year, month):
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        func.to_char(Expense.date, 'YYYY') == str(year),
        func.to_char(Expense.date, 'MM') == f'{month:02d}'
    ).order_by(Expense.date.asc()).all()
    total = sum(e.amount for e in expenses)
    month_name = f"{calendar.month_name[month]} {year}"
    return render_template('monthly_detail.html', expenses=expenses,
                           total=round(total, 2), month_name=month_name)


@app.route('/yearly')
@login_required
def yearly():
    results = (
        db.session.query(
            func.to_char(Expense.date, 'YYYY').label('year'),
            func.sum(Expense.amount).label('total')
        )
        .filter_by(user_id=current_user.id)
        .group_by('year').order_by('year').all()
    )
    yearly_data = [{'year': int(r.year), 'total': round(r.total, 2)} for r in results]
    return render_template('yearly.html', yearly_data=yearly_data)


@app.route('/yearly/<int:year>')
@login_required
def yearly_detail(year):
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        func.to_char(Expense.date, 'YYYY') == str(year)
    ).order_by(Expense.date.asc()).all()
    total = sum(e.amount for e in expenses)
    cat_totals = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.user_id == current_user.id,
                func.to_char(Expense.date, 'YYYY') == str(year))
        .group_by(Expense.category).all()
    )
    cat_labels = [c[0] for c in cat_totals]
    cat_values = [round(c[1], 2) for c in cat_totals]
    return render_template('yearly_detail.html', expenses=expenses,
                           total=round(total, 2), year=year,
                           cat_labels=cat_labels, cat_values=cat_values)


@app.route('/filter')
@login_required
def filter_expenses():
    category = request.args.get('category', 'All')
    if category == 'All':
        expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    else:
        expenses = Expense.query.filter_by(user_id=current_user.id, category=category).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template('filter.html', expenses=expenses, total=round(total, 2),
                           categories=CATEGORIES, selected=category)


@app.route('/search')
@login_required
def search():
    search_type = request.args.get('type', '')
    value = request.args.get('value', '')
    expenses = []
    label = ''

    if search_type == 'year' and value:
        expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            func.to_char(Expense.date, 'YYYY') == value
        ).order_by(Expense.date.asc()).all()
        label = f'Year: {value}'
    elif search_type == 'month' and value:
        year, month = value.split('-')
        expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            func.to_char(Expense.date, 'YYYY') == year,
            func.to_char(Expense.date, 'MM') == month
        ).order_by(Expense.date.asc()).all()
        label = f'{calendar.month_name[int(month)]} {year}'
    elif search_type == 'date' and value:
        try:
            search_date = datetime.strptime(value, '%Y-%m-%d').date()
            expenses = Expense.query.filter_by(user_id=current_user.id, date=search_date).order_by(Expense.date.asc()).all()
            label = search_date.strftime('%d %b %Y')
        except ValueError:
            pass

    total = round(sum(e.amount for e in expenses), 2)
    return render_template('search.html', expenses=expenses, total=total,
                           label=label, search_type=search_type, value=value)


# ---------- INIT ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)