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
class Favorite: 
    def __init__(self, data):
        self.user_id = data['user_id']
        self.openmic_id = data['openmic_id']