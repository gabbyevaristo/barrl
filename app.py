from flask import Flask, render_template, redirect, request
from pi import pour_water
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        pour_water.pour_water()
        return redirect('/')
