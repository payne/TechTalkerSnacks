import os
from flask import Flask, render_template, redirect, url_for, request
from replit import web
from collections import Counter
from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField
from wtforms.validators import DataRequired

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!  From the index function"

# Example from 
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#rendering-templates
@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
  return render_template("hello.html", name=name)
  
prices = {
    'Rice Krispy Treats': 0.21,
    'candy': 0.50,
    'Propel': 0.45,
    'coke': 0.40,
    'celsius': 1.12
}

@app.route("/home/")
@web.authenticated
def home():
  users_database = web.UserStore().current
  purchases = users_database.get('purchases', [])
  deposits_list = users_database.get('deposits',[])
  total_spent, itemization = compute_total_spent(purchases)
  # Since the database doesn't like to store floats, we store strings
  deposit_amounts = [ float(deposit_string) for deposit_string in deposits_list ]
  balance = total_spent + sum(deposit_amounts)
  return render_template("home.html", prices = prices, balance = balance, itemization = itemization)

def compute_total_spent(purchases):
  items = [item for item in purchases]
  c = Counter(items)
  items_to_quantity_bought = { item: count for item, count in c.most_common() }
  ts = 0
  for item, count in items_to_quantity_bought.items():
    ts -= float(prices[item]) * count
  return ts, items_to_quantity_bought

@app.route("/buy")
@web.authenticated
def buy():
  item = request.args.get('item')
  users_database = web.UserStore().current
  purchases = users_database.get('purchases', [])
  purchases.append(item)
  users_database['purchases'] = purchases
  return redirect(url_for("home"))

class DepositForm(FlaskForm):
    amount = DecimalField('Money', validators=[DataRequired()])
    submit = SubmitField('Record Payment')
  
@app.route("/d", methods=['GET', 'POST'])
@web.authenticated
def deposit():
  users_database = web.UserStore().current
  deposits_list = users_database.get('deposits',[])
  form = DepositForm()
  if form.amount.data:
    amount = form.amount.data
    # Since the database doesn't like to store floats, we store strings
    deposits_list.append(f"{amount}")
    users_database['deposits'] = deposits_list
  return render_template("deposit.html", deposit_history = deposits_list, form=form)

@app.route("/history/")
@web.authenticated
def history():
  users_database = web.UserStore().current
  purchases = users_database.get('purchases', [])
  total_spent, itemization = compute_total_spent(purchases)
  return render_template("history.html", prices = prices, total_spent = total_spent, itemization = itemization)

@app.route('/clear', methods=['GET', 'POST'])
@web.authenticated
def clear():
    users = web.UserStore()
    if 'purchases' in users.current: del users.current['purchases']
    if 'deposits' in users.current: del users.current['deposits']
    return redirect(url_for("home"))
  

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'environment variable is set to an empty string'

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(host='0.0.0.0', port=8080)
