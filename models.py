from flask import Flask
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base
import settings
import stripe
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.TRACK_MODIFICATIONS

stripe.api_key = settings.STRIPE_SECRET_KEY # Stripe's API key

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(length=50))
    amount = Column(Float())
    description = Column(String(length=1000))
    time = Column(DateTime())

    def __init__(self, user_id, amount, description):
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.time = datetime.datetime.now()

    def __repr__(self):
        return '<user_id {} expense {}>'.format(self.user_id, amount)

class Income(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(length=50))
    amount = Column(Float())
    description = Column(String(length=1000))
    time = Column(DateTime())

    def __init__(self, user_id, amount, description):
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.time = datetime.datetime.now()

    def __repr__(self):
        return '<user_id {} income {}>'.format(self.user_id, amount)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    email = Column(String(length=120), unique=True)
    password = Column(String(length=50))
    verify = Column(Boolean())
    stripe_customer_id = Column(String(length=100))
    _customer = None

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.verify = True

    def customer(self):
        customer = stripe.Customer.retrieve(self.stripe_customer_id)
        self._customer = customer
        return customer

    def __repr__(self):
        return '<User email {}>'.format(self.email)

class Merchant(Base):
    __tablename__ = 'merchants'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    email = Column(String(length=120), unique=True)
    password = Column(String(length=50))
    verify = Column(Boolean())
    stripe_customer_id = Column(String(length=100))
    _customer = None

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.verify = True

    def customer(self):
        customer = stripe.Customer.retrieve(self.stripe_customer_id)
        self._customer = customer
        return customer

    def __repr__(self):
        return '<Merchant email {}>'.format(self.email)

class StockPurchase(Base):
    __tablename__ = 'stockpurchases'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(length=50))
    amount = Column(Float())
    quantity = Column(Float())
    time = Column(DateTime())

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount
        self.time = datetime.datetime.now()

    def __repr__(self):
        return '<user_id {} expense {}>'.format(self.user_id, amount)

class CustomerPurchase(Base):
    __tablename__ = 'customerpurchase'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(length=50))
    amount = Column(Float())
    merchant_id = Column(String(length=50))
    stripe_charge_id = Column(String(length=50))
    stripe_payout_id = Column(String(length=50))
    time = Column(DateTime())

    def __init__(self, user_id, amount, merchant_id, stripe_charge_id, stripe_payout_id):
        self.user_id = user_id
        self.amount = amount
        self.merchant_id = merchant_id
        self.stripe_charge_id = stripe_charge_id
        self.stripe_payout_id = stripe_payout_id
        self.time = datetime.datetime.now()

    def __repr__(self):
        return '<customer_purchase {} customer {} merchant {}>'.format(self.id, self.user_id, self.merchant_id)
