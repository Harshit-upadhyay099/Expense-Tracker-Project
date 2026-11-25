from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    kind = db.Column(db.String(10), nullable=False)  # Income or Expense
    txn_date = db.Column(db.Date, nullable=False, default=date.today)
    note = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<Transaction {self.title}>"

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Health",
              "Entertainment", "Salary", "Freelance", "Other"]

@app.context_processor
def inject_globals():
    return {"categories": CATEGORIES, "today": date.today().isoformat()}

@app.route("/")
def dashboard():
    income = db.session.query(func.sum(Transaction.amount)).filter_by(kind="Income").scalar() or 0
    expenses = db.session.query(func.sum(Transaction.amount)).filter_by(kind="Expense").scalar() or 0
    balance = income - expenses
    recent = Transaction.query.order_by(Transaction.txn_date.desc(), Transaction.id.desc()).limit(8).all()

    rows = (db.session.query(Transaction.category, func.sum(Transaction.amount))
            .filter_by(kind="Expense")
            .group_by(Transaction.category).all())
    category_labels = [r[0] for r in rows]
    category_values = [round(r[1], 2) for r in rows]

    month = date.today().month
    year = date.today().year
    month_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.kind == "Income",
        func.strftime("%m", Transaction.txn_date) == f"{month:02d}",
        func.strftime("%Y", Transaction.txn_date) == str(year)).scalar() or 0
    month_expenses = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.kind == "Expense",
        func.strftime("%m", Transaction.txn_date) == f"{month:02d}",
        func.strftime("%Y", Transaction.txn_date) == str(year)).scalar() or 0

    return render_template("dashboard.html", income=income, expenses=expenses, balance=balance,
                           recent=recent, category_labels=category_labels,
                           category_values=category_values, month_income=month_income,
                           month_expenses=month_expenses)

@app.route("/transactions")
def transactions():
    kind = request.args.get("kind", "All")
    query = Transaction.query
    if kind in ("Income", "Expense"):
        query = query.filter_by(kind=kind)
    items = query.order_by(Transaction.txn_date.desc(), Transaction.id.desc()).all()
    return render_template("transactions.html", transactions=items, selected_kind=kind)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "Other")
        kind = request.form.get("kind", "Expense")
        date_text = request.form.get("txn_date", "")
        note = request.form.get("note", "").strip()

        try:
            amount = float(amount_text)
            txn_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            if not title or amount <= 0 or kind not in ("Income", "Expense"):
                raise ValueError
        except (ValueError, TypeError):
            flash("Please enter valid transaction details. Amount must be greater than zero.", "error")
            return redirect(url_for("add_transaction"))

        db.session.add(Transaction(title=title, amount=amount, category=category,
                                    kind=kind, txn_date=txn_date, note=note))
        db.session.commit()
        flash("Transaction added successfully.", "success")
        return redirect(url_for("transactions"))
    return render_template("add_transaction.html")

@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    item = Transaction.query.get_or_404(transaction_id)
    db.session.delete(item)
    db.session.commit()
    flash("Transaction deleted.", "success")
    return redirect(url_for("transactions"))

@app.route("/reports")
def reports():
    income = db.session.query(func.sum(Transaction.amount)).filter_by(kind="Income").scalar() or 0
    expenses = db.session.query(func.sum(Transaction.amount)).filter_by(kind="Expense").scalar() or 0
    rows = (db.session.query(Transaction.category, func.sum(Transaction.amount))
            .filter_by(kind="Expense").group_by(Transaction.category).all())
    labels = [r[0] for r in rows]
    values = [round(r[1], 2) for r in rows]
    return render_template("reports.html", income=income, expenses=expenses,
                           labels=labels, values=values)

@app.route("/seed-demo")
def seed_demo():
    if Transaction.query.count() == 0:
        demo = [
            Transaction(title="Monthly Salary", amount=25000, category="Salary", kind="Income", txn_date=date.today().replace(day=1)),
            Transaction(title="Freelance Work", amount=4500, category="Freelance", kind="Income", txn_date=date.today()),
            Transaction(title="Groceries", amount=1800, category="Food", kind="Expense", txn_date=date.today()),
            Transaction(title="Bus and Auto", amount=650, category="Travel", kind="Expense", txn_date=date.today()),
            Transaction(title="Internet Bill", amount=799, category="Bills", kind="Expense", txn_date=date.today()),
            Transaction(title="College Books", amount=1200, category="Education", kind="Expense", txn_date=date.today()),
        ]
        db.session.add_all(demo)
        db.session.commit()
        flash("Sample transactions added.", "success")
    else:
        flash("Sample data was not added because transactions already exist.", "error")
    return redirect(url_for("dashboard"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
