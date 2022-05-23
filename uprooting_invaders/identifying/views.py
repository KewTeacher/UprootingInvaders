
from flask import Flask, Blueprint, flash, render_template, request, url_for, redirect, session
from flask import current_app
from werkzeug.utils import secure_filename
import requests
import json
import os
import logging
import sys
import pymongo
from bson import ObjectId

# Blueprint Configuration
identifying = Blueprint(
    'identifying', __name__,
    template_folder='templates',
    static_folder='static'
)
#Uploading data stuff
UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

API_KEY = "2b10FP9NjPISdGPyjNBrQowG"	# Plant API_KEY here
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"



client = pymongo.MongoClient(os.getenv("DB_CONNECTION"))
db = client.get_database('uprooting_invaders')
allplants = db.all_plants
findings = db.findings

"""
data = {
    'organs': ['flower', 'leaf']
}

files = [
	('images', (image_path, image_data)),
]

req = requests.Request('POST', url=api_endpoint, files=files, data=data)
prepared = req.prepare()
s = requests.Session()
response = s.send(prepared)
json_result = json.loads(response.text)
"""

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@identifying.route('/upload', methods=['GET', 'POST'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





#API stuff
API_KEY = "2b10FP9NjPISdGPyjNBrQowG"	# Plant API_KEY here
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


def run_api(name):
    image_path = "static/uploads/"+ name
    image_data = open(image_path, 'rb')

    data = {
	'organs': ['leaf']
}

    files = [
	('images', (image_path, image_data)),
]
    print(str(data), file=sys.stdout)
    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()

    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    #json_result.results[0:3]

    #print(response.status_code)
    #print(json_result, file=sys.stdout)
    return json_result, image_path


def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

 #   req = requests.get('https://cat-fact.herokuapp.com/facts')
 #   req = requests.Request('POST', url=api_endpoint, files=files, data=data)
     #datas = json.loads(req.results)
    #global currentfilename
     #run_api(currentfilename)
#Plant ID stuff
@identifying.route('/plantid', methods=['POST', 'GET'])
def plantid():
    if request.method == "POST":

            # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            #json_result={}
            #image_data=""
            json_result, image_path = run_api(filename)
            #json_result[0:2]
            data=json_result["results"][0:3]

           # print(str(data) , file=sys.stdout)
            #this is where you can run a loop to query the all plants collection
            # loop though data and append if invasive
            for i in data:
                #find the plant on the allplants collection
                print('********************', file=sys.stdout)
                print('info from api', file=sys.stdout)
                print(i , file=sys.stdout)
                plant_found = allplants.find_one({"Scientific Name with Author": {'$regex': i['species']['scientificNameWithoutAuthor']}})
                #find out if it's invasive
                print('info from db', file=sys.stdout)
                print(plant_found, file=sys.stdout)
                try:
                    i['Inv'] = plant_found['Inv']
                except:
                    print('non invasive', file=sys.stdout)

                #if so add the Inv data to i

                #May need multiple inserts to the mongo db since we need to insert the email, data on the plant, etc.
                #findings.insert_one({'content': conent, 'degree': degree})

            return render_template('plantid.html', data=data, image=image_path,imagename=filename, email=session["email"])
        return data,session["email"]
    else:
        return render_template('upload.html', email=session["email"])



@identifying.route('/savingid', methods=['POST', 'GET'])
def save_findings():

    plantfinding={"loc":{}}
    plantfinding["loc"]["latitude"]=request.form.get("lat")
    plantfinding["loc"]["longitude"]=request.form.get("lng")
    plantfinding["Common Name"] = request.form.get("Common Name")
    try:
        plantfinding["Inv"]=json.loads(request.form.get("Inv"))
    except:
        print("not invasive", file=sys.stdout)
    plantfinding["Image"]=request.form.get("Image")
    plantfinding['Scientific Name With Author'] = request.form.get('Scientific Name With Author')
    print(plantfinding, file=sys.stdout)
    #print("coords", file=sys.stdout)
    #print(coords, file=sys.stdout)
    #plantfinding["loc"]["latitude"]=coords["latitude"]
    #plantfinding["loc"]["longitude"]=coords["longitude"]
    plantfinding['User']=ObjectId(session['id'])
    #plantfinding['image']=image
    #plantfinding['data']=data



    #This should be the code we need to insert coordinates into the MongoDB
    findings.insert_one(plantfinding)


    return redirect(url_for("map.home"), code=303)
    #return reder_template('maps.html')
