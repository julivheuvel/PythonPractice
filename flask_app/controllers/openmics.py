# ==================
# STANDARD IMPORTS
# ==================
from flask_app import app
from flask import render_template, request, redirect, session

# ==================
# MODEL IMPORTS
# ==================
from flask_app.models.openmic import OpenMic
from flask_app.models.user import User

# ==================
# REDIRECT ATTRIBUTES FOR FLASH MESSAGES
# ==================
from flask import flash

# ==================
# CREATE OPENMIC ROUTE
# ==================
# RENDER
@app.route("/openmics/create")
def create_openmic():

    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")

    user_id = session["user_id"]

    return render_template("new_openmic.html", user_id = user_id)

# POST
@app.route("/create-openmic", methods=['POST'])
def new_openmic():

    # Validating info
    if not OpenMic.validate_openmic(request.form):
        return redirect('/openmics/create')

    # pass back data
    data = {
        "venue" : request.form["venue"],
        "type" : request.form["type"],
        "date" : request.form["date"],
        "description" : request.form["description"],
        "user_id" : request.form["user_id"]
    }
    OpenMic.save(data)

    return redirect("/dashboard")

# ==================
# VIEW OPENMIC ROUTE
# ==================
@app.route("/openmics/<int:id>")
def view_one(id):
    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")

    # pass back data to view one specific event based on route
    data = {
        "id" : id
    }

    openmic = OpenMic.one_openmic(data)
    
    return render_template("view_openmic.html", openmic = openmic)

# ==================
# EDIT OPENMIC ROUTE
# ==================
# RENDER
@app.route("/openmics/edit/<int:id>")
def edit_one(id):
    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")

    # pass back data to view one specific event based on route
    data = {
        "id" : id
    }

    openmic = OpenMic.one_openmic(data)
    
    return render_template("edit_openmic.html", openmic = openmic)

# POST
@app.route("/edit-openmic/<int:id>", methods=['POST'])
def update_openmic(id):

    # Validating info
    if not OpenMic.validate_openmic(request.form):
        return redirect(f"/openmics/edit/{id}")

    # pass back data
    data = {
        "venue" : request.form["venue"],
        "type" : request.form["type"],
        "date" : request.form["date"],
        "description" : request.form["description"],
        "id" : id
    }
    OpenMic.update_openmic(data)
    return redirect("/dashboard")


# ==================
# DELETE OPENMIC ROUTE
# ==================
@app.route("/openmics/delete/<int:id>")
def delete_openmic(id):
    data = {
        "id" : id

    }
    OpenMic.delete(data)

    return redirect("/dashboard")