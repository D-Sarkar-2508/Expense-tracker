# 💸 Expense Tracker

<div align="center">

![Expense Tracker Banner](https://img.shields.io/badge/Expense-Tracker-6366f1?style=for-the-badge&logo=python&logoColor=white)

**A sleek, full-featured personal finance tracker built with Flask & PostgreSQL**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

</div>

---

<div align="center">

[![Click Here to Open 👉](https://img.shields.io/badge/Click%20Here%20to%20Open%20👉-Live%20Demo-FF6B6B?style=for-the-badge)](https://expense-tracker-v9a6.onrender.com)

</div>

---

## ✨ Features

- ➕ **Add / Edit / Delete** expenses with title, amount, category, date & notes
- 📊 **Interactive Doughnut Chart** — spending breakdown by category
- 📅 **Monthly Summary** — bar chart with month-by-month analysis
- 📆 **Yearly Summary** — year-by-year overview with category breakdown
- 🔍 **Smart Search** — search by year, month, or exact date
- 🏷️ **Filter by Category** — instantly filter across 8 categories
- 💾 **Cloud Database** — powered by Supabase PostgreSQL
- 🌐 **Live Deployed** — accessible from anywhere via Render
- 📱 **Responsive Design** — works on mobile and desktop
- 🌙 **Dark Theme** — easy on the eyes with a modern Catppuccin-inspired palette

---

## 🖥️ Live Demo

🔗 **[https://expense-tracker-v9a6.onrender.com](https://expense-tracker-v9a6.onrender.com)**

> ⚠️ Hosted on Render's free tier — the app may take **~30 seconds to wake up** on the first visit if it has been inactive.

---

## 📸 Screenshots

| Home Page | Monthly Summary |
|-----------|----------------|
| Add expenses, view chart & table | Bar chart with clickable months |

| Yearly Summary | Search & Filter |
|----------------|----------------|
| Year-over-year breakdown | Search by date, month, or year |

---

## 🗂️ Project Structure

```
Expense_tracker/
│
├── app.py                  # Flask app — routes & database logic
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── .env                    # Environment variables (not in repo)
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css       # Dark theme stylesheet
│
└── templates/
    ├── base.html           # Base layout with navbar
    ├── index.html          # Home — add expense + chart + table
    ├── edit.html           # Edit expense form
    ├── monthly.html        # Monthly summary + bar chart
    ├── monthly_detail.html # Expenses for a specific month
    ├── yearly.html         # Yearly summary + bar chart
    ├── yearly_detail.html  # Expenses for a specific year
    ├── filter.html         # Filter by category
    └── search.html         # Search by year / month / date
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/D-Sarkar-2508/Expense-tracker.git
cd Expense-tracker
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root folder:
```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

### 5. Run the app
```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Database** | PostgreSQL (Supabase) |
| **ORM** | Flask-SQLAlchemy |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Charts** | Chart.js |
| **Deployment** | Render |
| **Version Control** | Git & GitHub |

---

## 📦 Dependencies

```
flask
flask-sqlalchemy
psycopg2-binary
python-dotenv
gunicorn
```

---

## 🏷️ Expense Categories

| Category | | Category | |
|----------|--|----------|--|
| 🍔 Food | | 🏥 Health | |
| 🚌 Transport | | 🎬 Entertainment | |
| 🛍️ Shopping | | 📄 Bills | |
| 📚 Education | | 📦 Other | |

---

## 👩‍💻 Author

**Ditipriya Sarkar**

[![GitHub](https://img.shields.io/badge/GitHub-D--Sarkar--2508-181717?style=flat-square&logo=github)](https://github.com/D-Sarkar-2508)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ and Flask

⭐ Star this repo if you found it useful!

</div>
