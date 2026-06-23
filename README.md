<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=6366f1&height=200&section=header&text=💸%20Expense%20Tracker&fontSize=50&fontColor=ffffff&fontAlignY=38&desc=Track%20every%20rupee.%20Own%20your%20finances.&descAlignY=58&descSize=18" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

<br/>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Click%20Here-6366f1?style=for-the-badge&logoColor=white)](https://expense-tracker-v9a6.onrender.com)
<br/>

> **A full-stack personal finance web app** — built with Flask & PostgreSQL, featuring multi-user authentication, interactive charts, and smart expense filtering across daily, monthly, and yearly views.

<br/>

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **User Authentication** | Register, login, logout — each user sees only their own data |
| ➕ **Add / Edit / Delete** | Full CRUD for expenses with title, amount, category, date, note |
| 📊 **Category Chart** | Interactive doughnut chart — click a slice to filter by category |
| 📅 **Monthly View** | Bar chart with year selector — click any bar to see that month's expenses |
| 📆 **Yearly View** | Year-by-year spending with per-year category breakdown |
| 🔍 **Smart Search** | Search expenses by exact year, month, or date |
| 🏷️ **Category Filter** | Filter all expenses by 8 built-in categories |
| 💰 **Summary Cards** | Total Spent, Total Entries, Categories Used — all clickable |
| 🌑 **Dark Theme** | Fully dark, modern UI with color-coded category badges |
| ☁️ **Cloud Database** | Supabase PostgreSQL — data persists across devices per user |

---

## 🛠️ Tech Stack

```
Frontend      →   HTML5, CSS3, JavaScript, Chart.js
Backend       →   Python, Flask, Flask-Login, SQLAlchemy
Database      →   PostgreSQL (Supabase)
Auth          →   Flask-Login + Werkzeug password hashing
Deployment    →   Render (Web Service)
```

---

## 📁 Project Structure

```
Expense_tracker/
│
├── app.py                  ← Flask app — all routes & models
├── requirements.txt        ← Python dependencies
├── render.yaml             ← Render deployment config
├── .env                    ← Environment variables (not pushed)
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css       ← Dark theme stylesheet
│
└── templates/
    ├── base.html           ← Shared navbar & layout
    ├── login.html          ← Login page
    ├── register.html       ← Register page
    ├── index.html          ← Home dashboard
    ├── edit.html           ← Edit expense form
    ├── filter.html         ← Filter by category
    ├── monthly.html        ← Monthly summary + chart
    ├── monthly_detail.html ← Single month expenses
    ├── yearly.html         ← Yearly summary + chart
    ├── yearly_detail.html  ← Single year expenses
    └── search.html         ← Search by date/month/year
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/D-Sarkar-2508/Expense-tracker.git
cd Expense-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file:
```env
DATABASE_URL=postgresql://your_supabase_connection_string
SECRET_KEY=your_secret_key
```

### 4. Run the app
```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 🗄️ Database Schema

```sql
-- Users table
CREATE TABLE public."user" (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(80)  UNIQUE NOT NULL,
    email    VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

-- Expenses table
CREATE TABLE public.expense (
    id       SERIAL PRIMARY KEY,
    title    VARCHAR(100) NOT NULL,
    amount   FLOAT        NOT NULL,
    category VARCHAR(50)  NOT NULL,
    date     DATE         NOT NULL,
    note     VARCHAR(200),
    user_id  INTEGER REFERENCES public."user"(id)
);
```

---

## 🏷️ Expense Categories

<div align="center">

![Food](https://img.shields.io/badge/🍕%20Food-f9e2af?style=flat-square&labelColor=2a1e0f&color=2a1e0f)
![Transport](https://img.shields.io/badge/🚌%20Transport-89dceb?style=flat-square&labelColor=0f1e2a&color=0f1e2a)
![Shopping](https://img.shields.io/badge/🛍️%20Shopping-f38ba8?style=flat-square&labelColor=2a0f1e&color=2a0f1e)
![Health](https://img.shields.io/badge/💊%20Health-a6e3a1?style=flat-square&labelColor=0f2a1e&color=0f2a1e)
![Entertainment](https://img.shields.io/badge/🎬%20Entertainment-cba6f7?style=flat-square&labelColor=1e0f2a&color=1e0f2a)
![Bills](https://img.shields.io/badge/📄%20Bills-fab387?style=flat-square&labelColor=2a1e0f&color=2a1e0f)
![Education](https://img.shields.io/badge/📚%20Education-94e2d5?style=flat-square&labelColor=0f2a2a&color=0f2a2a)
![Other](https://img.shields.io/badge/📦%20Other-a6adc8?style=flat-square&labelColor=1e1e1e&color=1e1e1e)

</div>

---

## ☁️ Deployment

This app is deployed on **Render** with **Supabase PostgreSQL**.

| Service | Role |
|---|---|
| [Render](https://render.com) | Hosts the Flask web service |
| [Supabase](https://supabase.com) | Cloud PostgreSQL database |

Live URL → **[https://expense-tracker-v9a6.onrender.com](https://expense-tracker-v9a6.onrender.com)**

---

## 👩‍💻 Developer

<div align="center">

**Ditipriya Sarkar**
3rd Year B.Tech CSE (AI/ML) — Brainware University, Kolkata

[![GitHub](https://img.shields.io/badge/GitHub-D--Sarkar--2508-181717?style=for-the-badge&logo=github)](https://github.com/D-Sarkar-2508)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-6366f1?style=for-the-badge&logo=vercel&logoColor=white)](https://d-sarkar-2508.github.io/D-Sarkar-2508.Portfolio/)
[![Email](https://img.shields.io/badge/Email-ditipriya2508@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ditipriya2508@gmail.com)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=6366f1&height=100&section=footer" width="100%"/>

⭐ **Star this repo if you found it helpful!**

</div>
