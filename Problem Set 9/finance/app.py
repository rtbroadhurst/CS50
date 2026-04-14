import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def cash_for(user_id):
    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    return rows[0]["cash"]


def shares_for(user_id, symbol):
    rows = db.execute(
        """
        SELECT COALESCE(SUM(shares), 0) AS total_shares
        FROM transactions
        WHERE user_id = ? AND symbol = ?
        """,
        user_id,
        symbol
    )
    return rows[0]["total_shares"]


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    rows = db.execute(
        """
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
        ORDER BY symbol
        """,
        user_id
    )

    stocks = []
    holdings_total = 0

    for row in rows:
        quote = lookup(row["symbol"])
        if not quote:
            continue

        shares = row["total_shares"]
        price = quote["price"]
        total = shares * price
        holdings_total += total

        stocks.append(
            {
                "symbol": quote["symbol"],
                "name": quote["name"],
                "shares": shares,
                "price": price,
                "total": total,
            }
        )

    cash = cash_for(user_id)
    grand_total = cash + holdings_total

    return render_template("index.html", stocks=stocks, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        if not shares_input:
            return apology("must provide shares", 400)

        try:
            shares = int(shares_input)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]
        cash = cash_for(user_id)
        cost = shares * quote["price"]

        if cost > cash:
            return apology("can't afford", 400)

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id,
            quote["symbol"],
            shares,
            quote["price"]
        )

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash - cost,
            user_id
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    transactions = db.execute(
        """
        SELECT symbol, shares, price, transacted_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted_at DESC, id DESC
        """,
        user_id
    )

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)

        if not stock:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if not confirmation:
            return apology("must confirm password", 400)

        if password != confirmation:
            return apology("passwords must match", 400)

        hash_value = generate_password_hash(password)

        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hash_value
            )
        except ValueError:
            return apology("username already exists", 400)

        session["user_id"] = user_id

        return redirect("/")

    return render_template("register.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        amount_input = request.form.get("amount")

        if not amount_input:
            return apology("must provide amount", 400)

        try:
            amount = float(amount_input)
        except ValueError:
            return apology("amount must be a number", 400)

        if amount <= 0:
            return apology("amount must be positive", 400)

        user_id = session["user_id"]
        current_cash = cash_for(user_id)

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            current_cash + amount,
            user_id
        )

        return redirect("/")

    return render_template("add_cash.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    owned = db.execute(
        """
        SELECT symbol
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
        ORDER BY symbol
        """,
        user_id
    )

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")

        if not symbol:
            return apology("must select symbol", 400)

        if not shares_input:
            return apology("must provide shares", 400)

        try:
            shares = int(shares_input)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        current_shares = shares_for(user_id, symbol)

        if current_shares <= 0:
            return apology("you do not own that stock", 400)

        if shares > current_shares:
            return apology("too many shares", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        proceeds = shares * quote["price"]
        cash = cash_for(user_id)

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id,
            quote["symbol"],
            -shares,
            quote["price"]
        )

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash + proceeds,
            user_id
        )

        return redirect("/")

    return render_template("sell.html", owned=owned)
