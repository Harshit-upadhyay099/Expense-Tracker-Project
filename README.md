# Expense Tracker — Python + HTML + CSS

A college-ready personal expense management web application built with Flask, SQLite, HTML, CSS and Chart.js.

## Features
- Dashboard with total income, total expenses and current balance
- Add income and expense transactions
- Category selection, date and optional note
- View all transactions and filter by type
- Delete transactions
- Expense category chart and report summary
- SQLite database created automatically
- Optional demo data

## Requirements
- Python 3.9 or newer
- Internet connection for the Chart.js CDN charts (the rest of the app runs locally)

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted `expense_tracker_project` folder.
3. In the folder address bar, type `cmd` and press Enter.
4. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
5. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the app:
   ```bash
   python app.py
   ```
7. Open this address in your browser:
   `http://127.0.0.1:5000`

## Add sample data
After starting the app, open:
`http://127.0.0.1:5000/seed-demo`

Sample data is inserted only if the database is empty.

## Project structure
```text
expense_tracker_project/
├── app.py
├── requirements.txt
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── add_transaction.html
    ├── transactions.html
    └── reports.html
```

## Database
SQLite database file `instance/expense_tracker.db` is generated automatically on first run. Each transaction stores title, amount, category, type, date and note.

## Academic project overview
**Objective:** To provide a simple digital system for recording and reviewing personal income and expenses.

**Technology used:** Python (Flask), HTML5, CSS3, SQLite, SQLAlchemy and Chart.js.

**Future scope:** User login, recurring transactions, monthly budgets, CSV/PDF export and cloud deployment.
