from flask import Flask, render_template

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
  
@app.route("/home/")
def home():
  prices = {
      'Rice Krispy Treats': 0.21,
      'candy': 0.50,
      'Propel': 0.45,
      'coke': 0.40,
      'celsius': 1.12
  }
  return render_template("home.html", prices = prices)
  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
