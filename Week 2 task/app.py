from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product Model

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Integer, nullable=False)

    category = db.Column(db.String(100), nullable=False)

    image = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

# Home Route

@app.route('/')
def home():

    featured_products = Product.query.limit(3).all()

    return render_template(
        'index.html',
        products=featured_products
    )

# Products Route With Search

@app.route('/products')
def products():

    search = request.args.get('search')

    if search:

        all_products = Product.query.filter(
            Product.name.contains(search) |
            Product.category.contains(search)
        ).all()

    else:

        all_products = Product.query.all()

    return render_template(
        'products.html',
        products=all_products
    )

# Product Details Route

@app.route('/product/<int:id>')
def product_details(id):

    product = Product.query.get_or_404(id)

    return render_template(
        'product_details.html',
        product=product
    )

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)