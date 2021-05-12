from flask import Flask, render_template, redirect, request, session, flash
from pi import pour_water
from menu import drinks
import json

app = Flask(__name__)
app.secret_key = "hello"


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pour_water.pour_water()
        return redirect('/')
    else:
        return render_template('index.html')


@app.route('/menu', methods=["GET", "POST"])
def menu():
    return render_template('menu.html', drinks=drinks)


@app.route('/shopping-cart')
def cart():
    if "shopping_cart" not in session:
        return render_template('cart.html', drinks={})
    else:
        return render_template('cart.html', drinks=drinks)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    