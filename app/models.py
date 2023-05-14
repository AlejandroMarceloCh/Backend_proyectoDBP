from app import db, app, loginManager, bcrypt
from flask_login import UserMixin


@loginManager.user_loader
def load_user(id):
     return User.query.get(int(id))


#Models
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35),)
    email = db.Column(db.String(35),nullable=False, unique = True)
    password = db.Column(db.String(64), nullable=False)


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
         return bcrypt.check_password_hash(self.password, password)


    def __repr__(self):
        return f"USER {self.id} : {self.name}"
         

with app.app_context():
        db.create_all()
