import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "FirstTimeUsingFlask"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

    def seed(): 
        items = [
            Item(name='Dragon Ball: Volume 1', description='Manga volume by Akira Toriyama', image='DB_1.png', price=7.99, author='Akira Toriyama'),
            Item(name='Dragon Ball: Volume 3', description='Manga volume by Akira Toriyama', image='DB_3.jpg', price=7.99, author='Akira Toriyama'),
            Item(name='Jujutsu Kaisen: Volume 1', description='Manga volume by Gege Akutami', image='JJK_!.PNG', price=8.99, author='Gege Akutami'),
            Item(name='Hunter X Hunter: Volume 1', description='Manga volume by Yoshihiro Togashi', image='HXH_1.PNG', price=8.99, author='Yoshihiro Togashi'),
        ]
        db.session.bulk_save_objects(items)
        db.session.commit()

with app.app_context():
    db.create_all()
    if not Item.query.first():
        Item.seed()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/manga')
def manga():
    sort = request.args.get('sort', 'name')
    if sort == 'price':
        items = Item.query.order_by(Item.price).all()
    elif sort == 'eco':
        items = Item.query.order_by(Item.eco_impact).all()
    else:
        items = Item.query.order_by(Item.name).all()
    return render_template('manga.html', items=items, sort=sort)

@app.route('/product/<int:id>')
def product(id):
    item = Item.query.get_or_404(id)
    return render_template('Product.html', item=item)

@app.route('/basket')
def basket():
    basket = session.get('basket', [])
    items = []
    total = 0
    for item_id in basket:
        item = Item.query.get(item_id)
        if item:
            items.append(item)
            total += item.price
    return render_template('basket.html', items=items, total=total)

@app.route('/remove/<int:id>')
def remove_from_basket(id):
    if 'basket' in session:
        session['basket'].remove(id)
        session.modified = True
    return redirect(url_for('basket'))

@app.route('/add/<int:id>', methods=['POST'])
def add_to_basket(id):
    if 'basket' not in session:
        session['basket'] = []
    session['basket'].append(id)
    session.modified = True
    return {'success': True}

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    basket = session.get('basket', [])
    total = 0
    for item_id in basket:
        item = Item.query.get(item_id)
        if item:
            total += item.price
    return render_template('checkout.html', total=total)

@app.route('/checkout/success')
def checkout_success():
    session.pop('basket', None)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)