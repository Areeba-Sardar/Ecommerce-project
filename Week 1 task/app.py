from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product/<id>')
def product_details(id):
    return render_template('product_details.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)