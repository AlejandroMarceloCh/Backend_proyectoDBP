from app import app, db
from app.models import User, Client, Product, Inventory, Purchase, Sale
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    return render_template("users.html",
        tittle = "Users", 
        users = User.query.all()
        )

@app.route("/sale")
def sale():
    return render_template("sale.html")

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for("purchase"))

    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
        
            with app.app_context():
                u = User(name, email, password)
                db.session.add(u)
                db.session.commit()

        except:
            flash("Error creating Employee", "danger")

    return render_template("signup.html", tittle = "Signup")


@app.route("/signupclient", methods=["GET", "POST"])
def signupclient():
    
    if current_user.is_authenticated:
        return redirect(url_for("sale"))

    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            with app.app_context():
                u = Client(name, email, password)
                db.session.add(u)
                db.session.commit()

        except:
            flash("Error creating Client", "danger")

    return render_template("signupclient.html", tittle = "SignupClient")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("purchase"))

    if request.method == "POST":
        with app.app_context():
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.query.filter_by(email=email).first()

            if user:    
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for("purchase"))
                else:
                    flash("Wrong password", "danger")

            else:
                flash("User with this email does not exist", "danger")
            
    return render_template("login.html", tittle = "Login")



@app.route('/loginclient', methods=['GET', 'POST'])
def loginclient():
    #Cambiar la redireccion a la interfaz que muestra los inventarios en lugar de index
    if current_user.is_authenticated:
        return redirect(url_for("sale"))


    if request.method == "POST":
        with app.app_context():
            email = request.form.get("email")
            password = request.form.get("password")
            user = Client.query.filter_by(email=email).first()

            if user: 
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for("sale")) #este "index" hace referencia a la funcion "index" de la linea 7
                else:
                    flash("Wrong password", "danger")

            else:
                flash("User with this email does not exist", "danger")
            
    return render_template("loginclient.html", tittle = "LoginClient")


@app.route("/makepurchase")
def makepurchase():
    #falta agregar la logica para meter las compras
    return render_template("makepurchase.html")


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    logout_user()
    return redirect(url_for("index"))


