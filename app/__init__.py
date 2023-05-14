from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)


USER_DB = 'postgres'
PASS_DB = '1234'
URL_DB = 'localhost:5432'
NAME_DB = 'tienda'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'


db              =   SQLAlchemy(app)
migrate         =   Migrate(app, db)
loginManager    =   LoginManager(app)
bcrypt          =   Bcrypt(app)


from app import models, routes


if __name__ == "__main__":
    app.run(debug=True)
