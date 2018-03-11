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
from flask_socketio import SocketIO, emit
import eventlet

app = Flask(__name__)

app.config['APP_SETTINGS'] = settings.APP_SETTINGS
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.TRACK_MODIFICATIONS
app.secret_key = settings.SECRET_KEY

stripe.api_key = settings.STRIPE_SECRET_KEY # Stripe's API key
socketio = SocketIO(app)


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

@app.route('/merchant/post', methods=["POST"])
def merchant_login_post():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        u = Merchant.query.filter_by(email=email).count()
        if u == 0:
            return redirect(url_for('.home_page'))
        user = Merchant.query.filter_by(email=email).first()
        print(user, file=sys.stderr)
        if not password == user.password:
            return redirect(url_for('.home_page'))
        session['merchant_csrf'] = json.dumps({"user":user.id})
        print(session['merchant_csrf'], file=sys.stderr)
        return redirect("/merchant/cc/" + str(user.id))

@app.route('/signout')
def signout():
    session.pop('csrf', None)
    return redirect("/")

@app.route('/')
def home_page():
    try:
        csrf = session.get('csrf', {})
        if len(csrf) == 0:
            return render_template("landing.html")
        uid = csrf[csrf.index(":")+2:len(csrf)-1]
        print(uid, file=sys.stderr)
        
        exc_info = sys.exc_info()
        user = User.query.filter_by(id=uid).first()
        print(user, file=sys.stderr)
        income_statements = Income.query.filter_by(user_id=user.id).all()
        print(income_statements, file=sys.stderr)
        new_income_statements = []
        income_total = 0
        for k in income_statements:
            new_income_statements.append({"amount": k.amount})
            income_total += k.amount
        expense_statements = Expense.query.filter_by(user_id=user.id).all()
        new_expense_statements = []
        expense_total = 0
        for k in expense_statements:
            new_expense_statements.append({"amount": k.amount, "description": k.description, "time": k.time.strftime("%Y-%m-%d %H:%M:%S")})
            expense_total += k.amount
        print(expense_statements, file=sys.stderr)
        if income_total == 0:
            income_total = 0.01
        expense_rate = int((expense_total/income_total)* 100)
        return render_template("index.html", user_id=user.id, user_name=user.name,
                                income=new_income_statements, expense=new_expense_statements, expense_rate=expense_rate)
    except:
        print("ERROR OCCURED", file=sys.stderr)
        print(traceback.print_exc())
        #session.pop('csrf', None)
        #return render_template("landing.html")

@app.route('/add/income', methods=["POST"])
def income_create():
    try:
        csrf = session.get('csrf', {})
        uid = csrf[csrf.index(":")+2:len(csrf)-1]
        print(uid, file=sys.stderr)
        if len(csrf) == 0:
            return render_template("index.html")
        else:
            user = User.query.filter_by(id=uid).first()
            amount = float(request.form["amount"])
            description = "Income"
            print(user, file=sys.stderr)
            new_income_statement = Income(str(user.id), amount, description)
            db_session.add(new_income_statement)
            db_session.commit()
            print('Created Income Statement', file=sys.stderr)
            return redirect(url_for('.home_page'))
    except:
        print("ERROR OCCURED", file=sys.stderr)
        session.pop('csrf', None)
        return render_template("index.html")

@app.route('/alexa/income/<amount>', methods=["GET"])
def income_create_alexa(amount):
    user = User.query.filter_by(id=1).first()
    amount = float(amount)
    description = "Income"
    print(user, file=sys.stderr)
    new_income_statement = Income(str(1), amount, description)
    db_session.add(new_income_statement)
    db_session.commit()
    print('Created Income Statement', file=sys.stderr)
    return '{"success": "200"}'

@app.route('/alexa/expense/<amount>/<category>', methods=["GET"])
def expense_create_alexa(amount, category):
    user = User.query.filter_by(id=1).first()
    amount = float(amount)
    description = category # MAKE SURE THAT THIS IS CAPITAL
    print(user, file=sys.stderr)
    new_income_statement = Expense(str(1), amount, description)
    db_session.add(new_income_statement)
    db_session.commit()
    print('Created Expense Statement', file=sys.stderr)
    return '{"success": "200"}'

@app.route('/add/expense', methods=["POST"])
def expense_create():
    try:
        csrf = session.get('csrf', {})
        uid = csrf[csrf.index(":")+2:len(csrf)-1]
        print(uid, file=sys.stderr)
        if len(csrf) == 0:
            return render_template("index.html")
        else:
            user = User.query.filter_by(id=uid).first()
            amount = float(request.form["amount"])
            description = request.form["category"]
            print(user, file=sys.stderr)
            new_expense_statement = Expense(str(user.id), amount, description)
            db_session.add(new_expense_statement)
            db_session.commit()
            print('Created Expense Statement', file=sys.stderr)
            return redirect(url_for('.home_page'))
    except:
        print("ERROR OCCURED", file=sys.stderr)
        session.pop('csrf', None)
        return render_template("index.html")

@app.route('/register', methods=["GET"])
def register():
    return render_template("pages-register.html", merchant=False)

@app.route('/merchant/register', methods=["GET"])
def merchant_register():
    return render_template("pages-register.html", merchant=True)

@app.route('/merchant/register/create', methods=["POST"])
def merchant_create_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not email.index("@") > 0 and not email.index(".") > email.index("@"):
            return redirect(url_for('.home_page'))
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        u = Merchant.query.filter_by(email=email).count()
        if u == 0:
            new_merchant = Merchant(name, email, password)
            db_session.add(new_merchant)
            db_session.commit()
            print('Created Merchant', file=sys.stderr)
            return redirect(url_for('.home_page'))
        return redirect(url_for('.home_page'))

@app.route('/login', methods=["GET"])
def login():
    return render_template("pages-login.html", merchant=False)

@app.route('/merchant/login', methods=["GET"])
def merchant_login():
    return render_template("pages-login.html", merchant=True)

@app.route('/user/setCreditCard/<customer>/<uid>', methods=["GET"])
def add_stripe_customer(customer, uid):
    user = User.query.filter_by(id=uid).first()
    user.stripe_customer_id = customer
    db_session.add(user)
    db_session.commit()
    return redirect("/")

@app.route('/cc/<uid>', methods=["GET", "POST"])
def credit_card(uid):
    user = User.query.filter_by(id=int(uid)).first()
    return render_template("pages-cc.html", user=user.id)

@app.route('/merchant/cc/<uid>', methods=["GET", "POST"])
def merchant_credit_card(uid):
    merchant = Merchant.query.filter_by(id=int(uid)).first()
    return render_template("pages-cc-merchant.html")

@socketio.on('connect-to-merchant')
def connect_to_merchant(json):
    print(json, file=sys.stderr)
    namespace = "/merchant/cc/" + json["merchant"]
    user = User.query.filter_by(id=int(json["user"])).first()
    json["name"] = user.name
    socketio.emit('connect-to-user', json)

@socketio.on('start-transaction')
def allow_connect_to_merchant(json):
    socketio.emit('start-transaction', json)

@socketio.on('pay')
def allow_connect_to_merchant(json):
    socketio.emit('transaction-complete', json)


if __name__ == '__main__':
    socketio.run(app, debug=True)
