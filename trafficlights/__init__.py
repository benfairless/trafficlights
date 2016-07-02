from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# Initialise empty objects
db = SQLAlchemy()

# Function for initialising application
def create_app(config_name):

    # Create application object and load specific configuration.
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Bind SQLAlchemy object to Flask appliction object.
    db.init_app(app)

    # Add the main application blueprint into the Flask application object.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Add the api application blueprint into the Flask application object.
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Return the Flask application object, meaning that calling create_app is
    # enough to expose the Flask object.
    return app
