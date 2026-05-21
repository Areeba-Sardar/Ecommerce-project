from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login Manager

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

# User Model

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))

# Product Model

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Integer, nullable=False)

    category = db.Column(db.String(100), nullable=False)

    image = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

# User Loader

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# Home Route

@app.route('/')
def home():

    featured_products = Product.query.limit(3).all()

    return render_template(
        'index.html',
        products=featured_products
    )

# Products Route With Pagination

@app.route('/products')
def products():

    page = request.args.get('page', 1, type=int)

    search = request.args.get('search')

    if search:

        pagination = Product.query.filter(
            Product.name.contains(search) |
            Product.category.contains(search)
        ).paginate(
            page=page,
            per_page=4
        )

    else:

        pagination = Product.query.paginate(
            page=page,
            per_page=4
        )

    products = pagination.items

    return render_template(
        'products.html',
        products=products,
        pagination=pagination
    )

# Product Details

@app.route('/product/<int:id>')
def product_details(id):

    product = Product.query.get_or_404(id)

    return render_template(
        'product_details.html',
        product=product
    )

# Signup Route

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']

        password = generate_password_hash(
            request.form['password']
        )

        user = User(
            username=username,
            password=password
        )

        db.session.add(user)

        db.session.commit()

        flash('Account Created Successfully')

        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Route

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for('home'))

        flash('Invalid Username Or Password')

    return render_template('login.html')

# Logout

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('home'))

# Add Product

@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():

    if request.method == 'POST':

        product = Product(

            name=request.form['name'],

            price=request.form['price'],

            category=request.form['category'],

            image=request.form['image'],

            description=request.form['description']
        )

        db.session.add(product)

        db.session.commit()

        return redirect(url_for('products'))

    return render_template('add_product.html')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)