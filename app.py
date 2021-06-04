from flask import Flask, render_template, redirect, request, session, jsonify, url_for, abort, flash
from pi import jsonService, MenuService, IngredientService, PouringService
from datetime import timedelta
import json
import stripe


app = Flask(__name__)
app.secret_key = 'barrrrl'
app.permanent_session_lifetime = timedelta(hours=4)

# Configure Stripe API keys
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51IrKAPEx3ZnFyUF0TLud5ekbUAvIM6Cdvo7RZkGhfoSNKJBLkpF0WE6A5GNGedvZ8VyzpVFb5NF5tdPJRqXmfvmu003iF1LG6k'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51IrKAPEx3ZnFyUF0xExm1uVSSm9XzTELrGlQwLnioL1PZ7N2OnuQbxy6IkJj7Jb1j7j1PTvvsI2rR0ISXC2ypBXI00VKnWo9Cm'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

bottles = jsonService.loadJson(r'jsonFiles/ingredients.json')
drinks = jsonService.loadJson(r'jsonFiles/menu.json')
pump_map = IngredientService.getPumpMap()


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/admin-login', methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        # Confirm correct access code was inputted
        if request.form.get('code') == 'highball':
            session['admin_login'] = True
            return redirect('/admin')
        else:
            flash('Incorrect access code')
            return render_template('admin_login.html')
    else:
        if 'admin_login' in session:
            return redirect('/admin')
        else:
            return render_template('admin_login.html')


@app.route('/admin', methods=["GET"])
def admin():
    if 'admin_login' in session:
        return render_template('admin.html', bottles=order_bottles(bottles, pump_map), \
            drinks=drinks, pump_map=pump_map, pump_num=(len(pump_map) / 3), show='admin')
    else:
        return redirect('/admin-login')


@app.route('/logout', methods=["POST"])
def logout():
    if 'admin_login' in session:
        session.pop('admin_login', None)
    return jsonify({})


@app.route('/update-bottles/<id>', methods=["POST"])
def update_bottles(id):
    global bottles
    global pump_map
    name = request.form.get('name')
    mL = request.form.get('ml')
    brand = request.form.get('brand')
    drink_type = request.form.get('type')
    estimated_fill = request.form.get('fill')
    pump_num = pump_map.get(id)
    if pump_num == None:
        pump_num = int(request.form.get('pump_num'))
    if name:
        IngredientService.modifyIngredient(id, name, pump_num , int(mL), brand, drink_type, int(estimated_fill))
        IngredientService.modifyPumpMapp(id, pump_num)
        pump_map = IngredientService.getPumpMap()
        bottles = IngredientService.getAllIngredients()
        bottles = order_bottles(bottles, pump_map)
        flash(name + ' ingredient updated')
    return redirect('/admin')


@app.route('/add-ingredient', methods=["POST"])
def add_ingredient():
    global bottles
    global pump_map
    name = request.form.get('name')
    mL = request.form.get('ml')
    brand = request.form.get('brand')
    drink_type = request.form.get('type')
    estimated_fill = request.form.get('fill')
    if name:
        IngredientService.addIngredient(name, -1, int(mL), brand, drink_type, int(estimated_fill))
        bottles = IngredientService.getAllIngredients()
        bottles = order_bottles(bottles, pump_map)
        flash(name + ' ingredient added')
    return redirect('/admin')


@app.route('/delete-ingredient/<id>', methods=["POST"])
def delete_ingredient(id):
    global bottles
    global pump_map
    name = bottles[id]['name']
    IngredientService.removeIngredientByGuid(id)
    bottles = IngredientService.getAllIngredients()
    pump_map = IngredientService.getPumpMap()
    bottles = order_bottles(bottles, pump_map)
    flash(name + ' deleted')
    return redirect('/admin')


@app.route('/update-menu/<id>', methods=["POST"])
def update_menu(id):
    global drinks
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.form.get('image')
    if name and price and image:
        drinks[id]['name'] = name
        drinks[id]['price'] = float(price)
        drinks[id]['description'] = request.form.get('description')
        drinks[id]['image'] = image
        jsonService.saveJson(drinks, r'jsonFiles/menu.json')
        flash(name + ' updated')
    return redirect('/admin')


@app.route('/add-drink', methods=["POST"])
def add_drink():
    global drinks
    ingredients = {}
    for x in range(1,7):
        id = request.form.get(f'ing{x}')
        ml = request.form.get(f'ml{x}')
        if id and id != "none" and ml != 0:
            ingredients[id] = ml
    name = request.form.get('name')
    image = request.form.get('image')
    price = request.form.get('price')
    if ingredients and name and image and price:
        MenuService.addDrinkToMenu(name, ingredients, request.form.get('description'), float(price), image)
        drinks = MenuService.getMenu()
        flash(name + ' added')
    return redirect('/admin')


@app.route('/delete-drink/<id>', methods=["POST"])
def delete_drink(id):
    global drinks
    name = drinks[id]['name']
    if id in drinks:
        del drinks[id]
    MenuService.removeDrinkByGuid(id)
    flash(name + ' deleted')
    return redirect('/admin')


@app.route('/mvp', methods=["GET", "POST"])
def mvp():
    if request.method == "POST":
        print('Pouring predetermined drink')
        return redirect('/mvp')
    else:
        return render_template('mvp.html')


@app.route('/menu')
def menu():
    filtered_drinks = {k:v for k,v in drinks.items() if MenuService.isValidDrinkToPour(k)}
    if 'shopping_cart' not in session:
        return render_template('menu.html', drinks=filtered_drinks, cart_quantity='', show='customer')
    else:
        return render_template('menu.html', drinks=filtered_drinks, cart_quantity=session['cart_quantity'], show='customer')


@app.route('/cart')
def cart():
    if 'shopping_cart' not in session:
        return render_template('cart.html', drinks={}, cart_quantity='', show='customer')
    else:
        return render_template('cart.html', drinks=session['shopping_cart'], cart_quantity=session['cart_quantity'], show='customer')


@app.route('/pour-portal')
def pour_portal():
    # Clear shopping cart and cart quantity session when user first enters portal
    if 'shopping_cart' in session:
        session['pour_items'] = session['shopping_cart'].copy()
        session.pop('shopping_cart', None)
        session.pop('cart_quantity', None)

    if 'pour_items' not in session:
        return render_template('pour_portal.html', drinks={}, cart_quantity='', show='customer')
    else:
        return render_template('pour_portal.html', drinks=session['pour_items'], cart_quantity='')


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']
    drink_quantity = data['drink_quantity']

    session.modified = True
    if 'shopping_cart' not in session:
        session['shopping_cart'] = {}
        session['cart_quantity'] = '0'

    # If drink is already in cart, update quantity
    if drink_id not in session['shopping_cart']:
        session['shopping_cart'][drink_id] = drinks[drink_id].copy()
        session['shopping_cart'][drink_id]['quantity'] = drink_quantity
    else:
        new_quantity = int(session['shopping_cart'][drink_id]['quantity']) + int(drink_quantity)
        session['shopping_cart'][drink_id]['quantity'] = str(new_quantity)

    session['cart_quantity'] = get_cart_quantity()
    return jsonify(session['cart_quantity'])


@app.route('/edit-cart', methods=['POST'])
def edit_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']
    updated_quantity = data['updated_quantity']

    session.modified = True

    # Update quantity
    session['shopping_cart'][drink_id]['quantity'] = updated_quantity
    session['cart_quantity'] = get_cart_quantity()

    return jsonify(session['cart_quantity'])


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = json.loads(request.data)
    drink_id = data['drink_id']

    session.modified = True

    # Remove item from session
    del session['shopping_cart'][drink_id]
    session['cart_quantity'] = get_cart_quantity()

    # Render empty cart page and clear session if cart becomes empty
    if len(session['shopping_cart']) == 0:
        session.pop('shopping_cart', None)
        session.pop('cart_quantity', None)
        return jsonify('')

    return jsonify(session['cart_quantity'])


@app.route('/pour-drink', methods=['POST'])
def pour_drink():
    data = json.loads(request.data)
    drink_id = data['drink_id'] # This id is used to determine which drink to pour
    print(drinks[drink_id]['name'] + ' poured!')

    session.modified = True

    new_quantity = int(session['pour_items'][drink_id]['quantity']) - 1

    # Delete drink from pour_items session if quantity reaches 0, else
    # set the new quantity to old quantity minus 1
    if new_quantity == 0:
        del session['pour_items'][drink_id]
    else:
        session['pour_items'][drink_id]['quantity'] = str(new_quantity)

    print(drink_id)
    PouringService.pourDrink(drink_id)

    # Remove pour_items session if there are no more drinks on the pour page
    if len(session['pour_items']) == 0:
        session.pop('pour_items', None)
        return jsonify('')

    return jsonify({})


@app.route('/checkout-session', methods=['POST'])
def checkout_session():
    cart_items = get_cart_items()

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=cart_items,
            mode='payment',
            allow_promotion_codes=True,
            success_url=url_for('pour_portal', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cart', _external=True),
    )

    return jsonify(id=checkout_session.id, public_key=app.config['STRIPE_PUBLIC_KEY'])


@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
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
        return {}, 400
    except stripe.error.SignatureVertificationError as e:
        # Invalid signature
        return {}, 400

    # Handle checkout session completed event
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']

    return {}


def order_bottles(bottles, pump_map):
    new_bottles = {}
    sort = [-1 for x in range(1,7)]
    for key, value in bottles.items():
        if key in pump_map:
            sort[pump_map[key]] = key
    for key in sort:
        if key != -1:
            new_bottles[key] = bottles[key]
    for key, value in bottles.items():
        if key not in pump_map:
            new_bottles[key] = value
    return new_bottles


def get_cart_quantity():
    if 'shopping_cart' in session:
        return str(sum(int(drink['quantity']) for drink in session['shopping_cart'].values()))


def get_cart_items():
    if 'shopping_cart' in session:
        items, items_list = session['shopping_cart'].copy(), []
        for item in items:
            item_dict = {}
            item_dict['price_data'] = {'currency': 'usd', 'product_data': {'name': items[item]['name'], 'images': [items[item]['image']]}, 'unit_amount': int(float(items[item]['price']) * 100)}
            item_dict['quantity'] = int(items[item]['quantity'])
            item_dict['tax_rates'] = ['txr_1IrTYZEx3ZnFyUF0aZ43zasr']
            items_list.append(item_dict)
        return items_list



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
