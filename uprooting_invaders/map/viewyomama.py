from flask import Blueprint, render_template, session, request, Flask
from werkzeug.utils import secure_filename
from flask_googlemaps import GoogleMaps
from datetime import datetime
import pymongo
import bcrypt
import os
import requests
import googlemaps

# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)

@map.route('/maps')
def home():
    app = Flask(__name__)
    app.config['AIzaSyBUawhsXSBBvMpWVCywU1lUUtm6dDrwtME'] = "8JZ7i18MjFuM35dJHq70n3Hx4"
    GoogleMaps(app)


'''
{% extends "base.html" %}
{% block title %}Register System{% endblock %}

{% block content %}

<iframe width="800"
        height="600"
        style="border:0"
        loading="lazy"
        allowfullscreen
        referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps/embed/v1/place?key=AIzaSyBUawhsXSBBvMpWVCywU1lUUtm6dDrwtME
    &q=ip_address">
</iframe>

{% endblock %}

'''