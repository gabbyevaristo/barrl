from flask import Flask, render_template, redirect, request, session, jsonify,url_for, abort
from pi import pour_water
from menu import drinks
from datetime import timedelta
import json
import stripe


app = Flask(__name__)
app.secret_key = 'barrl'
app.permanent_session_lifetime = timedelta(minutes=5)

app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51IrKAPEx3ZnFyUF0TLud5ekbUAvIM6Cdvo7RZkGhfoSNKJBLkpF0WE6A5GNGedvZ8VyzpVFb5NF5tdPJRqXmfvmu003iF1LG6k"
app.config['STRIPE_SECRET_KEY'] = "sk_test_51IrKAPEx3ZnFyUF0xExm1uVSSm9XzTELrGlQwLnioL1PZ7N2OnuQbxy6IkJj7Jb1j7j1PTvvsI2rR0ISXC2ypBXI00VKnWo9Cm"
stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/menu', methods=["GET", "POST"])
def menu():
    if "shopping_cart" not in session:
        return render_template('menu.html', drinks=drinks, cart_quantity=None)
    else:
        return render_template('menu.html', drinks=drinks, cart_quantity=session["cart_quantity"])


@app.route('/cart')
def cart():
    if "shopping_cart" not in session:
        return render_template('cart.html', drinks={}, cart_quantity=None)
    else:
        return render_template('cart.html', drinks=session["shopping_cart"], cart_quantity=session["cart_quantity"])


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']
    drink_quantity = data['drink_quantity']

    session.modified = True
    if "shopping_cart" not in session:
        session["shopping_cart"] = {}
        session["cart_quantity"] = "0"

    # If drink is already in cart, update quantity
    if drink_id not in session["shopping_cart"]:    
        session["shopping_cart"][drink_id] = drinks[drink_id].copy()
        session["shopping_cart"][drink_id]['quantity'] = drink_quantity
    else:
        new_quantity = int(session["shopping_cart"][drink_id]['quantity']) + int(drink_quantity)
        session["shopping_cart"][drink_id]['quantity'] = str(new_quantity)
    
    session["cart_quantity"] = get_cart_quantity()
    return jsonify({})


@app.route('/edit-cart', methods=['POST'])
def edit_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']
    updated_quantity = data['updated_quantity']

    session.modified = True

    # Update quantity
    session["shopping_cart"][drink_id]['quantity'] = updated_quantity
    session["cart_quantity"] = get_cart_quantity()
    
    return jsonify({})


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']

    session.modified = True

    # Remove item from session
    del session["shopping_cart"][drink_id]
    session["cart_quantity"] = get_cart_quantity()

    # Render empty cart page and clear session if cart becomes empty
    if len(session["shopping_cart"]) == 0:
        session.pop("shopping_cart", None)
        session.pop("cart_quantity", None)
    
    return jsonify({})


@app.route('/pour-portal')
def pour_portal():
    return render_template('pour_portal.html')


@app.route('/checkout-session', methods=['POST'])
def checkout_session():
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'T-shirt',
            },
            'unit_amount': 2000,
        },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('pour_portal', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('menu', _external=True),
    )

    # Might still need session on pour page (can just hide cart)
    session.pop("shopping_cart", None)
    session.pop("cart_quantity", None)

    return jsonify(id=session.id, public_key=app.config['STRIPE_PUBLIC_KEY'])


@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_KQcUiBWfljqRFzN6AbqIKV6wb6s6bMd8'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print("INVALID PAYLOAD")
        return {}, 400
    except stripe.error.SignatureVertificationError as e:
        # Invalid signature
        print("INVALID SIGNATURE")
        return {}, 400
    
    # Handle checkout session completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        # line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        # print(line_items['data'][0['description'])

    return {}


def get_cart_quantity():
    if "shopping_cart" in session:
        return str(sum(int(drink['quantity']) for drink in session["shopping_cart"].values()))



if __name__ == "__main__":
    app.run(debug=True)
