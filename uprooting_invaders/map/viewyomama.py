from flask import Blueprint, render_template, session, request, Flask
from werkzeug.utils import secure_filename
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from datetime import datetime
import pymongo
import bcrypt
import os
import sys
import requests
from flask import current_app
#import googlemaps

# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)

client = pymongo.MongoClient(os.getenv("DB_CONNECTION"))
db = client.get_database('uprooting_invaders')
allplants = db.all_plants
findings = db.findings

@map.route('/maps')
def home():
    found = findings.find()
    invlist = []
    noninvlist = []



    for i in found:
        dict = {}
        print (i, file=sys.stdout)
        dict["lat"] = i["loc"] ["latitude"]
        dict["lng"] = i["loc"] ["longitude"]
        dict["infobox"] = "<P>"+i["Common Name"]+ " </P>"
        if "Inv" in i and len(i["Inv"]) > 0:
            dict["icon"] = image_path = 'static/invasive plants.png'
            invlist.append (dict)
        else:
            dict["icon"] = image_path = 'static/native plants.png'
            invlist.append (dict)
    #print (invlist, file=sys.stdout)
    #print (noninvlist, file=sys.stdout)

    map = Map(
        identifier="map",
        center_on_user_location=True,
        lat=0,
        lng=0,
        markers=invlist

    )
    return render_template('googlemap.html', map=map)
