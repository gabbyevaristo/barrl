from flask import Flask, render_template, redirect, request
from pi import pour_water
from menu import drinks
import json

app = Flask(__name__)

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


# @app.route('/getdrinklist')
# def get_python_data():
#     return json.dumps(drinks)


@app.route('/cart')
def cart():
    return render_template('cart.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")