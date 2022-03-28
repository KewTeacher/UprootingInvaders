from flask import Blueprint, render_template, session, request
from werkzeug.utils import secure_filename
import pymongo
import bcrypt
import os

# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)


@geo.route('/maps', methods = ['POST', 'GET'])

def hello():
    return 'Hello World'
