from flask import Blueprint, render_template, session, request, Flask
from werkzeug.utils import secure_filename
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from datetime import datetime
import pymongo
import bcrypt
import os
import requests
from flask import current_app
#import googlemaps

# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)


@map.route('/maps')
def home():

    map = Map(
        identifier="map",
        center_on_user_location=True,
        lat=0,
        lng=0,

    )
    return render_template('maps.html', map=map)



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
        src="https://www.google.com/maps/embed/v1/place?key=
    &q=ip_address">
</iframe>

{% endblock %}

'''
