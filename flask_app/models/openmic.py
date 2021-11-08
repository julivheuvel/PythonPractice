# ==================
# STANDARD IMPORTS
# ==================
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

# ==================
# MODEL IMPORTS
# ==================
from flask_app.models import user

# ==================
# REDIRECT ATTRIBUTES FOR FLASH MESSAGES
# ==================
from flask import flash


# ==================
# USER MODEL
# ==================
class OpenMic: 
    def __init__(self, data):
        self.id = data['id']
        self.venue = data['venue']
        self.type = data['type']
        self.date = data['date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # list of users who favorited this openmic
        self.users_who_favorited = []

        # get single instance of user who posted openmic
        self.posted_by = {}

    # ==================
    # VALIDATIONS
    # ==================
    @staticmethod
    def validate_openmic(data):
        is_valid = True
        if len(data['venue']) < 3:
            flash("Venue must be at least 3 characters long!")
            is_valid = False
        if len(data['type']) < 3:
            flash("Type must be at least 3 characters long!")
            is_valid = False
        if len(data['date']) < 6:
            flash("Date must be at least 6 characters long!")
            is_valid = False
        if len(data['description']) < 5:
            flash("Description must be at least 5 characters long!")
            is_valid = False
        return is_valid

    # ==================
    # SAVE/CREATE METHOD
    # ==================
    @classmethod
    def save(cls, data):
        query = "INSERT INTO openmics (venue, type, date, description, user_id, created_at, updated_at) VALUES (%(venue)s, %(type)s, %(date)s, %(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL("openmic_schema").query_db(query, data)
    
    # ==================
    # GET ALL METHOD
    # ==================
    @classmethod
    def all_openmics(cls):
        query = "SELECT * FROM openmics;"
        results = connectToMySQL('openmic_schema').query_db(query)
        
        openmics = []
        for one_openmic in results:
            openmics.append(cls(one_openmic))
        return openmics
    
    # ==================
    # VIEW ONE METHOD
    # ==================
    @classmethod
    def one_openmic(cls, data):
        query = "SELECT * FROM openmics JOIN users ON users.id = user_id WHERE openmics.id = %(id)s;"
        results = connectToMySQL('openmic_schema').query_db(query, data)
        
        openmic = cls(results[0])
        # pulling out specific data of the user object to store in posted_by
        user_data = {
            "id" : results[0]['users.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at'],
        }
        
        # posted_by = specific instance of user
        openmic.posted_by = user.User(user_data)
        return openmic
    
    # ==================
    # UPDATE ONE METHOD
    # ==================
    @classmethod
    def update_openmic(cls, data):
        query = "UPDATE openmics SET venue = %(venue)s, type = %(type)s, date = %(date)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL('openmic_schema').query_db(query, data)
        return results

    # ==================
    # DELETE ONE METHOD
    # ==================
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM openmics WHERE id = %(id)s;"
        results = connectToMySQL('openmic_schema').query_db(query, data)
        return results