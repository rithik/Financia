from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from models import Expense, Income, User, Merchant, StockPurchase, CustomerPurchase
import settings
import sys
from database import db_session
import json
from werkzeug.utils import secure_filename
import stripe
import traceback

app = Flask(__name__)

app.config['APP_SETTINGS'] = settings.APP_SETTINGS
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.TRACK_MODIFICATIONS
app.secret_key = settings.SECRET_KEY

#stripe.api_key = settings.STRIPE_SECRET_KEY # Stripe's API key

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/register/create', methods=["POST"])
def create_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not email.index("@") > 0 and not email.index(".") > email.index("@"):
            return redirect(url_for('.home_page'))
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        u = User.query.filter_by(email=email).count()
        if u == 0:
            new_user = User(name, email, password)
            db_session.add(new_user)
            db_session.commit()
            print('Created User', file=sys.stderr)
            return redirect(url_for('.home_page'))
        return redirect(url_for('.home_page'))

@app.route('/income/create', methods=["POST"])
def income_create():
    if request.method == "POST":
        csrf = session.get('csrf', {})
        if len(csrf) == 0:
            return render_template("index.html")
        else:
            user = User.query.filter_by(id=csrf).first()
            amount = request.form["amount"]
            description = request.form["description"]
            new_income_statement = Income(user_id, amount, description)
            db_session.add(new_income_statement)
            db_session.commit()
            print('Created Income Statement', file=sys.stderr)
            return redirect(url_for('.home_page'))

@app.route('/expense/create', methods=["POST"])
def expense_create():
    if request.method == "POST":
        csrf = session.get('csrf', {})
        if len(csrf) == 0:
            return render_template("index.html")
        else:
            user = User.query.filter_by(id=csrf).first()
            amount = request.form["amount"]
            description = request.form["description"]
            new_expense_statement = Expense(user_id, amount, description)
            db_session.add(new_expense_statement)
            db_session.commit()
            print('Created expense Statement', file=sys.stderr)
            return redirect(url_for('.home_page'))

@app.route('/login/post', methods=["POST"])
def login_post():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        u = User.query.filter_by(email=email).count()
        if u == 0:
            return redirect(url_for('.home_page'))
        user = User.query.filter_by(email=email).first()
        print(user, file=sys.stderr)
        if not password == user.password:
            return redirect(url_for('.home_page'))
        session['csrf'] = json.dumps({"user":user.id})
        print(session['csrf'], file=sys.stderr)
        return redirect(url_for('.home_page'))

@app.route('/')
def home_page():
    try:
        csrf = session.get('csrf', {})
        uid = csrf[csrf.index(":")+2:len(csrf)-1]
        print(uid, file=sys.stderr)
        if len(csrf) == 0:
            return render_template("index.html")
        else:
            exc_info = sys.exc_info()
            user = User.query.filter_by(email="rithik@gmail.com").first()
            print(user, file=sys.stderr)
            income_statements = Income.query.filter_by(user_id=user.id).all()
            print(income_statements, file=sys.stderr)
            expense_statements = Expense.query.filter_by(user_id=user.id).all()
            print(expense_statements, file=sys.stderr)
            return render_template("index.html", user_name=user.name,
                                    income=income_statements, expense=expense_statements)
    except:
        print("ERROR OCCURED", file=sys.stderr)
        session.pop('csrf', None)
        return render_template("index.html")

@app.route('/register', methods=["GET"])
def register():
    return render_template("pages-register.html")

@app.route('/login', methods=["GET"])
def login():
    return render_template("pages-login.html")

if __name__ == '__main__':
    app.run()
