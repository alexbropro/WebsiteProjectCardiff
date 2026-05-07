import os
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
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
    eco_impact = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<Item {self.name}>'

    def seed(): 
        items = [
            Item(name='Dragon Ball: Volume 1', description="Before there was \"Dragon Ball Z\", there was Akira Toriyama's action epic \"Dragon Ball\", starring the younger version of Son Goku and all the other \"Dragon Ball Z\" heroes! Meet a naive young monkey-tailed boy named Goku, whose quiet life changes when he meets Bulma, a girl who is on a quest to collect seven \"Dragon Balls.\" If she gathers them all, an incredibly powerful dragon will appear and grant her one wish. But the precious orbs are scattered all over the world, and Bulma needs Goku's help (and his super-strength)! With a magic staff for a weapon and a flying cloud for a ride, Goku sets out on the adventure of a lifetime…", image='DB_1.png', price=7.99, author='Akira Toriyama', eco_impact=2.5),
            Item(name='Dragon Ball: Volume 3', description='With the Dragon Balls gone and Bulma\'s summer vacation over, Goku goes to the remote house of the Turtle Hermit, Kame-Sen\'nin, to be trained in the martial arts. There, the girl-ogling old master promises to teach Goku everything he knows…and prepare him for the Tenka\'ichi Budôkai, the great tournament to determine the Strongest Fighter in the World! But Goku\'s fellow student, the Shaolin monk Kuririn, isn\'t above cheating to be the best. Can the two of them get along as they undergo the strangest martial arts training ever?', image='DB_3.jpg', price=7.99, author='Akira Toriyama', eco_impact=2.0),
            Item(name='Jujutsu Kaisen: Volume 1', description='Although Yuji Itadori looks like your average teenager, his immense physical strength is something to behold! Every sports club wants him to join, but Itadori would rather hang out with the school outcasts in the Occult Research Club. One day, the club manages to get their hands on a sealed cursed object. Little do they know the terror they will unleash when they break the seal...', image='JJK_1.PNG', price=8.99, author='Gege Akutami', eco_impact=1.8),
            Item(name='Hunter X Hunter: Volume 1', description='Gon Freecss has almost reached the age of twelve, the earliest age at which one is allowed to register for the Hunter Exam. Despite the objections of his aunt Mito (also his adoptive mother), Gon sets off to follow in the footsteps of his father, the legendary Hunter Ging Freecss.', image='HXH_1.PNG', price=8.99, author='Yoshihiro Togashi', eco_impact=2.2),
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
    return render_template('successpage.html')

@app.route('/api/item/<int:id>')
def item_api(id):
    item = Item.query.get_or_404(id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'author': item.author,
        'image': item.image,
        'eco_impact': item.eco_impact
    })


@app.route('/api/search')
def search_api():
    query = request.args.get('q', '')
    if query:
        results = Item.query.filter(
            (Item.name.ilike(f'%{query}%')) | 
            (Item.author.ilike(f'%{query}%'))
        ).all()
    else:
        results = []
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'author': item.author,
        'image': item.image,
        'price': item.price,
        'eco_impact': item.eco_impact
    } for item in results])


if __name__ == '__main__':
    app.run(debug=True)