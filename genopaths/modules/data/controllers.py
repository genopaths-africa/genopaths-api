from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, make_response
from genopaths.modules.parameters.models import Data, DataSchema
from genopaths.extensions import db
from genopaths import app
import datetime
from flask_login import login_required, login_manager
from datetime import datetime
import base64
from sqlalchemy import or_
from sqlalchemy.dialects import postgresql

mod_parameters = Blueprint('data', __name__, url_prefix='/api/data')

