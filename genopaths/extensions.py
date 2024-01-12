# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

# Import Flask Marshmallow
from flask_marshmallow import Marshmallow

# Login
from flask_login import user_loaded_from_request, user_loaded_from_request, LoginManager

ma = Marshmallow()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
seeder = FlaskSeeder()