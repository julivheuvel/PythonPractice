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