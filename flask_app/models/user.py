# ==================
# STANDARD IMPORTS
# ==================
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

# ==================
# MODEL IMPORTS
# ==================


# ==================
# REDIRECT ATTRIBUTES FOR FLASH MESSAGES
# ==================
from flask import flash

# ==================
# REGEX IMPORTS
# ==================
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# ==================
# BCRYPT IMPORTS
# ==================
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ==================
# USER MODEL
# ==================
class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ==================
    # VALIDATIONS
    # ==================
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters long!")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters long!")
            is_valid = False
        if len(data['email']) < 3:
            flash("Email must be at least 3 characters long!")
            is_valid = False
        if len(data['password']) < 5:
            flash("Password must be at least 5 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is not valid!")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid


    # ==================
    # GET EMAIL METHOD
    # ==================
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("openmic_schema").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    # ==================
    # SAVE/CREATE METHOD
    # ==================
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("openmic_schema").query_db(query, data)

    # ==================
    # GET ONE USER METHOD
    # ==================
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('openmic_schema').query_db(query, data)
        return cls(results[0])