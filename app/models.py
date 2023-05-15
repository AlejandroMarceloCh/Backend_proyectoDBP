from app import db, app, loginManager, bcrypt
from flask_login import UserMixin
from datetime import date


@loginManager.user_loader
def load_user(id):
     return User.query.get(int(id))


#Models

#Employee Model
class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35),)
    email = db.Column(db.String(35),nullable=False, unique = True)
    password = db.Column(db.String(64), nullable=False)
    purchases = db.relationship('Purchase', backref='employee', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
         return bcrypt.check_password_hash(self.password, password)


    def __repr__(self):
        return f"Employee {self.id} : {self.name} : {self.email}"
    

#Client Model
class Client(db.Model, UserMixin):
    __tablename__ = "Clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    email = db.Column(db.String(35),nullable=False, unique = True)
    password = db.Column(db.String(64), nullable=False)
    sales = db.relationship('Sale', backref='client', lazy=True)
    created_at = db.Column(db.Integer, nullable=False, default=date.today().year)
    modified_at = db.Column(db.Integer, nullable=False, default=date.today().year)
    

    def __init__(self, name, email, password,): #Acá falta meter el sales
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"Client {self.id} : {self.name} : {self.email}"


#Product Model
class Product(db.Model):
    __tablename__ = "Products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    expense = db.Column(db.Integer, nullable=False)
    #imagen = 
    created_at = db.Column(db.Integer, nullable=False, default=date.today().year)
    modified_at = db.Column(db.Integer, nullable=False, default=date.today().year)


    def __init__(self, name, stock, expense): #
        self.name = name
        self.stock = stock
        self.expense = expense

    def __repr__(self):
        return f"Product {self.id} : {self.name} : {self.stock}"



#Product Model
class Inventory(db.Model):
    __tablename__ = "Inventory"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)


#Purchases
class Purchase(db.Model):
    __tablename__ = "Purchases"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String, db.ForeignKey('Products.id'), nullable=False) #
    quantity = db.Column(db.Integer, nullable = False)
    amount = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)      #
    created_at = db.Column(db.Integer, nullable=False, default=date.today().year)
    modified_at = db.Column(db.Integer, nullable=False, default=date.today().year)


    def __init__(self, product_id, quantity, amount, employee_id):
        self.product_id = product_id
        self.quantity = quantity
        self.amount = amount
        self.employee_id = employee_id

    def __repr__(self):
        return f"Product {self.id} : {self.name} : {self.stock}"


#Sales
class Sale(db.Model):
    __tablename__ = "Sales"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    amount = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.String(36), db.ForeignKey('Clients.id'), nullable=False)
    created_at = db.Column(db.Integer, nullable=False, default=date.today().year)
    modified_at = db.Column(db.Integer, nullable=False, default=date.today().year)

    def __init__(self, product_id, quantity, amount, client_id):
        self.product_id = product_id
        self.quantity = quantity
        self.amount = amount
        self.client_id = client_id

    def __repr__(self):
        return f"Sale {self.id}: Product {self.product_id} - Quantity: {self.quantity} - Amount: {self.amount}"


with app.app_context():
        db.create_all()
