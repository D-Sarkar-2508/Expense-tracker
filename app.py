from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import func
from dotenv import load_dotenv
import os
load_dotenv()
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'expense-tracker-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.adyvolgkagyrzvidgkkg:Ditipriya2508@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- MODEL ----------
class Expense(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(100), nullable=False)
    amount   = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date     = db.Column(db.Date, nullable=False, default=date.today)
    note     = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Expense {self.title} ₹{self.amount}>'

CATEGORIES = ['Food', 'Transport', 'Shopping', 'Health', 'Entertainment', 'Bills', 'Education', 'Other']

# ---------- ROUTES ----------

@app.route('/')
def index():
    # All expenses ordered by date desc
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)

    # Totals per category
    cat_totals = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .all()
    )
    cat_labels = [c[0] for c in cat_totals]
    cat_values = [round(c[1], 2) for c in cat_totals]

    return render_template('index.html',
                           expenses=expenses,
                           total=round(total, 2),
                           categories=CATEGORIES,
                           cat_labels=cat_labels,
                           cat_values=cat_values)


@app.route('/add', methods=['POST'])
def add_expense():
    title    = request.form.get('title', '').strip()
    amount   = request.form.get('amount', '')
    category = request.form.get('category', '')
    date_str = request.form.get('date', '')
    note     = request.form.get('note', '').strip()

    # Validation
    if not title or not amount or not category or not date_str:
        flash('Please fill all required fields.', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash('Amount must be a positive number.', 'error')
        return redirect(url_for('index'))

    try:
        expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format.', 'error')
        return redirect(url_for('index'))

    expense = Expense(title=title, amount=amount, category=category,
                      date=expense_date, note=note)
    db.session.add(expense)
    db.session.commit()
    flash('Expense added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
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
def monthly():
    selected_year = request.args.get('year', str(datetime.now().year))
    
    # Get all available years for dropdown
    all_years = db.session.query(
        func.extract('year', Expense.date).label('year')
    ).group_by('year').order_by('year').all()
    available_years = [int(r.year) for r in all_years]

    results = (
        db.session.query(
            func.extract('year', Expense.date).label('year'),
            func.extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total')
        )
        .filter(func.extract('year', Expense.date) == int(selected_year))
        .group_by('year', 'month')
        .order_by('month')
        .all()
    )

    monthly_data = []
    for r in results:
        month_name = calendar.month_abbr[int(r.month)]
        monthly_data.append({
            'label': f"{month_name} {r.year}",
            'total': round(r.total, 2),
            'year': int(r.year),
            'month': int(r.month)
        })

    return render_template('monthly.html', monthly_data=monthly_data,
                           selected_year=int(selected_year),
                           available_years=available_years)

@app.route('/monthly/<int:year>/<int:month>')
def monthly_detail(year, month):
    import calendar
    expenses = Expense.query.filter(
        func.extract('year', Expense.date) == year,
        func.extract('month', Expense.date) == month
    ).order_by(Expense.date.asc()).all()
    total = sum(e.amount for e in expenses)
    month_name = f"{calendar.month_name[month]} {year}"
    return render_template('monthly_detail.html', expenses=expenses,
                           total=round(total, 2), month_name=month_name)
    
@app.route('/yearly')
def yearly():
    results = (
        db.session.query(
            func.extract('year', Expense.date).label('year'),
            func.sum(Expense.amount).label('total')
        )
        .group_by('year')
        .order_by('year')
        .all()
    )
    yearly_data = [{'year': int(r.year), 'total': round(r.total, 2)} for r in results]
    return render_template('yearly.html', yearly_data=yearly_data)


@app.route('/yearly/<int:year>')
def yearly_detail(year):
    expenses = Expense.query.filter(
        func.extract('year', Expense.date) == year
    ).order_by(Expense.date.asc()).all()
    total = sum(e.amount for e in expenses)

    # Category breakdown for that year
    cat_totals = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter(func.extract('year', Expense.date) == year)
        .group_by(Expense.category)
        .all()
    )
    cat_labels = [c[0] for c in cat_totals]
    cat_values = [round(c[1], 2) for c in cat_totals]

    return render_template('yearly_detail.html', expenses=expenses,
                           total=round(total, 2), year=year,
                           cat_labels=cat_labels, cat_values=cat_values)
    
    
@app.route('/filter')
def filter_expenses():
    category = request.args.get('category', 'All')
    if category == 'All':
        expenses = Expense.query.order_by(Expense.date.desc()).all()
    else:
        expenses = Expense.query.filter_by(category=category).order_by(Expense.date.desc()).all()

    total = sum(e.amount for e in expenses)
    return render_template('filter.html',
                           expenses=expenses,
                           total=round(total, 2),
                           categories=CATEGORIES,
                           selected=category)

@app.route('/search')
def search():
    search_type = request.args.get('type', '')  # year / month / date
    value = request.args.get('value', '')
    expenses = []
    total = 0
    label = ''

    if search_type == 'year' and value:
        expenses = Expense.query.filter(
            func.extract('year', Expense.date) == int(value)
        ).order_by(Expense.date.asc()).all()
        label = f'Year: {value}'

    elif search_type == 'month' and value:
        # value = "2026-06"
        year, month = value.split('-')
        expenses = Expense.query.filter(
            func.extract('year', Expense.date) == int(year),
            func.extract('month', Expense.date) == int(month)
        ).order_by(Expense.date.asc()).all()
        label = f'{calendar.month_name[int(month)]} {year}'

    elif search_type == 'date' and value:
        # value = "2026-06-21"
        try:
            search_date = datetime.strptime(value, '%Y-%m-%d').date()
            expenses = Expense.query.filter_by(date=search_date).order_by(Expense.date.asc()).all()
            label = f'{search_date.strftime("%d %b %Y")}'
        except ValueError:
            pass

    total = round(sum(e.amount for e in expenses), 2)
    return render_template('search.html', expenses=expenses,
                           total=total, label=label,
                           search_type=search_type, value=value)
    
    
# ---------- INIT ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)