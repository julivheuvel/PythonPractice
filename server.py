from flask_app import app

# Always import controllers as created
from flask_app.controllers import users










if __name__ == "__main__":
    app.run(debug=True)