from flask import Flask
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base
import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.TRACK_MODIFICATIONS

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(length=50))
    amount = Column(Float())
    description = Column(String(length=1000))

    def __init__(self, user_id, amount, description):
        self.user_id = user_id
        self.amount = amount
        self.description = description

    def __repr__(self):
        return '<email {} expense {}>'.format(self.email, amount)

class Income(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(length=50))
    amount = Column(Float())
    description = Column(String(length=1000))

    def __init__(self, user_id, amount, description):
        self.user_id = user_id
        self.amount = amount
        self.description = description

    def __repr__(self):
        return '<email {} income {}>'.format(self.email, amount)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    email = Column(String(length=120), unique=True)
    password = Column(String(length=50))
    verify = Column(Boolean())


    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.verify = True

    def __repr__(self):
        return '<email {}>'.format(self.email)

