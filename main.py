from flask import Flask, render_template, redirect, url_for, request
from replit import web
from collections import Counter

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
  total_spent, itemization = compute_total_spent(purchases)
  return render_template("home.html", prices = prices, total_spent = total_spent, itemization = itemization)

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

  
@app.route("/deposit/")
def deposit():
  return render_template("deposit.html")

@app.route("/history/")
def history():
  users_database = web.UserStore().current
  purchases = users_database.get('purchases', [])
  total_spent, itemization = compute_total_spent(purchases)
  return render_template("history.html", prices = prices, total_spent = total_spent, itemization = itemization)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
