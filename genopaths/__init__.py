# Import flask and template operators
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask.sessions import SecureCookieSessionInterface
from genopaths.extensions import db, ma, login_manager, migrate, seeder
from flask_login import UserMixin
from flask_cors import CORS
import base64
from flask_login import user_loaded_from_request, user_loaded_from_request
from flask import g
from genopaths.modules.users.models import User

# This prevents setting the Flask Session cookie whenever the user authenticated using your header_loader.
# Reference: https://flask-login.readthedocs.io/en/latest/
@user_loaded_from_request.connect    
def user_loaded_from_request(self, user=None):
    g.login_via_header = True


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

def create_app():
    # Define the WSGI application object
    app = Flask(__name__)

    # Disable strict forward slashed requirement
    app.url_map.strict_slashes = False

    # Configurations
    app.config.from_object('genopaths.config')

    # Define the database object which is imported
    # by modules and controllers
    db.init_app(app) #flask_sqlalchemy
    ma.init_app(app) #flask_marshmallow
    migrate.init_app(app, db)
    seeder.init_app(app, db) #flask-seeder
    
    # Enable CORS -- Remove this if not useful
    CORS(app,  origins="*")

    login_manager.init_app(app)

    # Disable sessions for API calls
    app.session_interface = CustomSessionInterface()

    return app


@login_manager.request_loader
def load_user_from_header(req):
    """Handle API authentication"""
    token = req.headers.get('Authorization')
    app.logger.info('ddd')
    if token is None:
        return None

    token = token.replace('Bearer ', '', 1)
    try:
        #token = base64.b64decode(token)
        #token = base64.b64decode(bytes(token, 'utf-8')).decode("utf-8")
        pass
    except TypeError:
        pass
    user = User.query.filter_by(token=token).first()
    if user:
        g.currentuser = user
        return user

    return None


# Initialize app and push application context so that extension can initiate the application context
app = create_app()
app.app_context().push()


# This is added to handle CORS
# Taken from https://mortoray.com/2014/04/09/allowing-unlimited-access-with-cors/
@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """

    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE, PATCH'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    # if app.debug:
    #    resp.headers['Access-Control-Max-Age'] = '1'

    return resp


# Intercept pre-flight requests
@app.before_request
def handle_options_header():
    if request.method == 'OPTIONS':
        headers = {}
        headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        headers['Access-Control-Allow-Credentials'] = 'true'
        headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
        headers['Access-Control-Allow-Headers'] = request.headers.get(
            'Access-Control-Request-Headers', 'Authorization')
        return '', 200, headers


# Import modules using the blueprint handlers variable (mod_vendors)
from genopaths.modules.users.controllers import mod_users as mod_users
from genopaths.modules.authentication.controllers import mod_auth as mod_auth
from genopaths.modules.projects.controllers import mod_projects as mod_projects
from genopaths.modules.parameters.controllers import mod_parameters as mod_parameters

# Register blueprint(s)
app.register_blueprint(mod_users)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_projects)
app.register_blueprint(mod_parameters)

# TP error handling
@app.errorhandler(404)
def not_found(error):
    #return render_template('404.html'), 404
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)
    
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')
