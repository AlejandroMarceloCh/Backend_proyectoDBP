from app import app, db
from app.models import User
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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    if current_user.is_authenticated:
        return redirect(url_for("index"))

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
            flash("Error creating user", "danger")

    return render_template("signup.html", tittle = "Signup")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        with app.app_context():
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.query.filter_by(email=email).first()

            if user:    
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for("index")) #este "index" hace referencia a la funcion "index" de la linea 7
                else:
                    flash("Wrong password", "danger")

            else:
                flash("User with this email does not exist", "danger")
            
    return render_template("login.html", tittle = "Login")

@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    logout_user()
    return redirect(url_for("index"))

