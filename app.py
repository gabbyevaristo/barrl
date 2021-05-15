from flask import Flask, render_template, redirect, request, session, jsonify
from pi import pour_water
from menu import drinks
from datetime import timedelta
import json

app = Flask(__name__)
app.secret_key = 'barrrrl'
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/menu', methods=["GET", "POST"])
def menu():
    return render_template('menu.html', drinks=drinks)


@app.route('/cart')
def cart():
    if "shopping_cart" not in session:
        return render_template('cart.html', drinks={})
    else:
        return render_template('cart.html', drinks=session["shopping_cart"])


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']
    drink_quantity = data['drink_quantity']

    session.modified = True
    if "shopping_cart" not in session:
        session["shopping_cart"] = {}

    # If drink is already in cart, update quantity
    if drink_id not in session["shopping_cart"]:    
        session["shopping_cart"][drink_id] = drinks[drink_id].copy()
        session["shopping_cart"][drink_id]['quantity'] = drink_quantity
    else:
        new_quantity = int(session["shopping_cart"][drink_id]['quantity']) + int(drink_quantity)
        session["shopping_cart"][drink_id]['quantity'] = str(new_quantity)
    
    return jsonify({})


@app.route('/edit-cart', methods=['POST'])
def edit_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']
    updated_quantity = data['updated_quantity']

    session.modified = True

    # Update quantity
    session["shopping_cart"][drink_id]['quantity'] = updated_quantity
    
    return jsonify({})


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']

    session.modified = True

    # Remove item from session
    del session["shopping_cart"][drink_id]

    # Render empty cart page and clear session if cart becomes empty
    if len(session["shopping_cart"]) == 0:
        session.pop("shopping_cart", None)
    
    return jsonify({})


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
