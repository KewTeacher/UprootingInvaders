from flask import Blueprint, render_template, session, request, Flask
from werkzeug.utils import secure_filename
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from datetime import datetime
import pymongo
import bcrypt
import os
import requests
#import googlemaps

# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)
#map.config['AIzaSyBUawhsXSBBvMpWVCywU1lUUtm6dDrwtME'] = "8JZ7i18MjFuM35dJHq70n3Hx4"
#GoogleMaps(map)

@map.route('/maps')
def home():
    #app = Flask(__name__)

    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('map.html', mymap=mymap, sndmap=sndmap)



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
