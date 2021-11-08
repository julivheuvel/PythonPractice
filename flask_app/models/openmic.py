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