from app import app, db, Product

with app.app_context():

    product1 = Product(
        name='Nike Shoes',
        price=120,
        category='Shoes',
        image='shoe.jpg',
        description='Premium quality sports shoes'
    )

    product2 = Product(
        name='Smart Watch',
        price=80,
        category='Watch',
        image='watch.jpg',
        description='Modern smart watch with cool features'
    )

    product3 = Product(
        name='Headphones',
        price=50,
        category='Electronics',
        image='headphone.jpg',
        description='Noise cancelling headphones'
    )

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)

    db.session.commit()

    print("Products Added Successfully")