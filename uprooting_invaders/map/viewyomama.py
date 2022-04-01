from flask import Blueprint, render_template, session, request, Flask
from werkzeug.utils import secure_filename
import pymongo
import bcrypt
import os
import requests

# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)

def get_country(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        country = js['countryCode']
        return country
    except Exception as e:
        return "Unknown"

@map.route('/maps')
def home():
    ip_address = request.remote_addr
    country = get_country(ip_address)
    # number of countries where the largest number of speakers are French
    # data from http://download.geonames.org/export/dump/countryInfo.txt
    if country in ('BL', 'MF', 'TF', 'BF', 'BI', 'BJ', 'CD', 'CF', 'CG', 'CI', 'DJ', 'FR', 'GA', 'GF', 'GN', 'GP', 'MC', 'MG', 'ML', 'MQ', 'NC'):
        return "Bonjour"
    return "Hello"
