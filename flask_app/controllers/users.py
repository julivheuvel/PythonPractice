# ==================
# STANDARD IMPORTS
# ==================
from flask_app import app
from flask import render_template, request, redirect, session


# ==================
# MODEL IMPORTS
# ==================
from flask_app.models.user import User
from flask_app.models.openmic import OpenMic


# ==================
# BCRYPT IMPORTS
# ==================
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ==================
# REDIRECT ATTRIBUTES FOR FLASH MESSAGES
# ==================
from flask import flash


# ==================
# INDEX ROUTE
# ==================
@app.route("/")
def index():
    return render_template("index.html")


# ==================
# REGISTER ROUTE
# ==================
@app.route("/register", methods=['POST'])
def register():
    # Validating info
    if not User.validate_user(request.form):
        return redirect('/')

    # check to see if email exists
    verify_for_existing_email = {
        "email" : request.form["email"]
    }
    if User.get_by_email(verify_for_existing_email):
        flash("Email already exists. Please use different email to complete registration")
        return redirect('/')

    # hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    # pass back data
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }

    # save data to database
    new_user_id = User.save(data)

    # pass information into session
    session["user_id"] = new_user_id

    return redirect("/dashboard")


# ==================
# LOGIN ROUTE
# ==================
# RENDER
@app.route("/login")
def login():
    return render_template("login.html")

# POST
@app.route("/logging-in", methods=['POST'])
def logging():
    # checking for existing email
    data = {
        "email" : request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credentials")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credentials")
        return redirect("/login")

    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


# ==================
# DASHBOARD ROUTE
# ==================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")
    
    # get logged in user information
    data = {
        "id" : session["user_id"]
    }
    user = User.get_one(data)

    # get all openmic info
    openmics = OpenMic.all_openmics()

    return render_template("dashboard.html", user = user, openmics = openmics)

# ==================
# LOGOUT ROUTE
# ==================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")