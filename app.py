from flask import Flask, render_template, redirect, request, url_for, session, jsonify, abort, flash
from pi import IngredientService, MenuService, PouringService
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


bottles = IngredientService.getIngredients(r'jsonFiles/ingredients.json')
drinks = MenuService.getMenu(r'jsonFiles/menu.json')
pump_map = IngredientService.getPumpMap()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/mvp', methods=['GET', 'POST'])
def mvp():
    if request.method == 'POST':
        print('Pouring predetermined drink')
        return redirect('/mvp')
    else:
        return render_template('mvp.html')



''' Admin routes '''

@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
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


@app.route('/admin', methods=['GET'])
def admin():
    if 'admin_login' in session:
        return render_template('admin.html', bottles=order_bottles(bottles, pump_map), \
            drinks=drinks, pump_map=pump_map, pump_num=(len(pump_map) / 3), nav_bar='admin')
    else:
        return redirect('/admin-login')


@app.route('/logout', methods=['POST'])
def logout():
    if 'admin_login' in session:
        session.pop('admin_login', None)
    return jsonify({})


@app.route('/update-bottles/<id>', methods=['POST'])
def update_bottles(id):
    global bottles, pump_map
    name = request.form.get('name')
    ml = request.form.get('ml')
    brand = request.form.get('brand')
    drink_type = request.form.get('type')
    estimated_fill = request.form.get('fill')

    # Get pump number if bottle is connected to a pump, else get the
    # pump number from form
    pump_num = pump_map.get(id)
    if pump_num == None:
        pump_num = int(request.form.get('pump_num'))

    IngredientService.modifyIngredient(id, name, pump_num, int(ml), brand, drink_type, int(estimated_fill))
    IngredientService.modifyPumpMap(id, pump_num)
    bottles = IngredientService.getIngredients()
    bottles = order_bottles(bottles, pump_map)
    pump_map = IngredientService.getPumpMap()
    flash('%s ingredient updated' % name)
    return redirect('/admin')


@app.route('/add-ingredient', methods=['POST'])
def add_ingredient():
    global bottles
    name = request.form.get('name')
    ml = request.form.get('ml')
    brand = request.form.get('brand')
    drink_type = request.form.get('type')
    estimated_fill = request.form.get('fill')

    IngredientService.addIngredient(name, -1, int(ml), brand, drink_type, int(estimated_fill))
    bottles = IngredientService.getIngredients()
    bottles = order_bottles(bottles, pump_map)
    flash('%s ingredient added' % name)
    return redirect('/admin')


@app.route('/delete-ingredient/<id>', methods=['POST'])
def delete_ingredient(id):
    global bottles, pump_map
    name = bottles[id]['name']
    IngredientService.removeIngredientByGuid(id)
    # Reload pump map in case deleted ingredient was in map
    pump_map = IngredientService.getPumpMap()
    bottles = IngredientService.getIngredients()
    bottles = order_bottles(bottles, pump_map)
    flash('%s deleted' % name)
    return redirect('/admin')


@app.route('/update-menu/<id>', methods=['POST'])
def update_menu(id):
    global drinks
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image = request.form.get('image')

    MenuService.modifyDrink(id, name, drinks[id]['ings'], description, float(price), image)
    drinks = MenuService.getMenu()
    flash('%s updated' % name)
    return redirect('/admin')


@app.route('/add-drink', methods=['POST'])
def add_drink():
    global drinks
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image = request.form.get('image')
    ingredients = {}
    for x in range(1,7):
        id = request.form.get(f'ing{x}')
        ml = request.form.get(f'ml{x}')
        if id and id != 'none' and ml != 0:
            ingredients[id] = ml

    MenuService.addDrinkToMenu(name, ingredients, description, float(price), image)
    drinks = MenuService.getMenu()
    flash('%s added' % name)
    return redirect('/admin')


@app.route('/delete-drink/<id>', methods=['POST'])
def delete_drink(id):
    global drinks
    name = drinks[id]['name']
    MenuService.removeDrinkByGuid(id)
    drinks = MenuService.getMenu()
    flash('%s deleted' % name)
    return redirect('/admin')



''' Customer routes '''

@app.route('/menu', methods=['GET'])
def menu():
    # Get only the drinks that are pourable
    filtered_drinks = {id: drink for id, drink in drinks.items() if MenuService.isValidDrinkToPour(id)}
    if 'shopping_cart' not in session:
        return render_template('menu.html', menu=filtered_drinks, nav_bar='customer')
    else:
        return render_template('menu.html', menu=filtered_drinks, cart_quantity=session['cart_quantity'], nav_bar='customer')


@app.route('/cart', methods=['GET'])
def cart():
    if 'shopping_cart' not in session:
        return render_template('cart.html', cart={}, show='customer')
    else:
        return render_template('cart.html', cart=session['shopping_cart'], cart_quantity=session['cart_quantity'], nav_bar='customer')


@app.route('/pour-portal', methods=['GET'])
def pour_portal():
    # Set pour session and clear cart session when customer first enters portal
    if 'shopping_cart' in session:
        session['pour_items'] = session['shopping_cart'].copy()
        session.pop('shopping_cart', None)
        session.pop('cart_quantity', None)

    if 'pour_items' not in session:
        return render_template('pour_portal.html', pour_drinks={}, nav_bar='customer')
    else:
        return render_template('pour_portal.html', pour_drinks=session['pour_items'])


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = json.loads(request.data)
    id = data['id']
    quantity = data['quantity']

    session.modified = True
    if 'shopping_cart' not in session:
        session['shopping_cart'] = {}
        session['cart_quantity'] = 0

    # Add drink id to cart if id is not in cart, else update drink id quantity
    if id not in session['shopping_cart']:
        session['shopping_cart'][id] = drinks[id].copy()
        session['shopping_cart'][id]['quantity'] = int(quantity)
    else:
        new_quantity = session['shopping_cart'][id]['quantity'] + int(quantity)
        session['shopping_cart'][id]['quantity'] = new_quantity

    session['cart_quantity'] = get_cart_quantity()
    return jsonify(session['cart_quantity'])


@app.route('/edit-cart', methods=['POST'])
def edit_cart():
    data = json.loads(request.data)
    id = data['id']
    updated_quantity = data['updated_quantity']

    session.modified = True
    session['shopping_cart'][id]['quantity'] = updated_quantity
    session['cart_quantity'] = get_cart_quantity()
    return jsonify(session['cart_quantity'])


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = json.loads(request.data)
    id = data['id']

    session.modified = True
    del session['shopping_cart'][id]
    if len(session['shopping_cart']) == 0:
        session.pop('shopping_cart', None)
        session.pop('cart_quantity', None)
        return jsonify('')

    session['cart_quantity'] = get_cart_quantity()
    return jsonify(session['cart_quantity'])


@app.route('/pour-drink', methods=['POST'])
def pour_drink():
    data = json.loads(request.data)
    id = data['id']

    session.modified = True
    updated_quantity = session['pour_items'][id]['quantity'] - 1

    # Delete drink id from pour session if id quantity reaches 0, else set
    # the new quantity to old quantity minus 1
    if updated_quantity == 0:
        del session['pour_items'][id]
    else:
        session['pour_items'][id]['quantity'] = updated_quantity

    PouringService.pourDrink(id)
    print('%s poured!' % drinks[id]['name'])

    if len(session['pour_items']) == 0:
        session.pop('pour_items', None)
        return jsonify('')

    return jsonify({})


@app.route('/checkout-session', methods=['POST'])
def checkout_session():
    line_items = get_line_items()
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
            mode='payment',
            allow_promotion_codes=True,
            success_url=url_for('pour_portal', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cart', _external=True),
    )
    return jsonify(id=checkout_session.id, public_key=app.config['STRIPE_PUBLIC_KEY'])


@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    if request.content_length > 1024 * 1024:
        print('Request too big!')
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
        return sum(int(drink['quantity']) for drink in session['shopping_cart'].values())


def get_line_items():
    if 'shopping_cart' in session:
        cart, line_items = session['shopping_cart'].copy(), []
        for id, drink in cart.items():
            item_dict = {}
            item_dict['price_data'] = {'currency': 'usd', 'product_data': {'name': drink['name'], 'images': [drink['image']]}, 'unit_amount': int(float(drink['price']) * 100)}
            item_dict['quantity'] = drink['quantity']
            item_dict['tax_rates'] = ['txr_1IrTYZEx3ZnFyUF0aZ43zasr']
            line_items.append(item_dict)
        return line_items



if __name__ == '__main__':
    app.run(debug=True)
