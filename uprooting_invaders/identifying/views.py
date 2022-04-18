
from flask import Flask, Blueprint, flash, render_template, request, url_for, redirect, session
from flask import current_app 
from werkzeug.utils import secure_filename
import requests
import json
import os
import logging
import sys

# Blueprint Configuration
identifying = Blueprint(
    'identifying', __name__,
    template_folder='templates',
    static_folder='static'
)
#Uploading data stuff
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

API_KEY = "2b10FP9NjPISdGPyjNBrQowG"	# Plant API_KEY here
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

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
    image_path = "uploads/"+ name
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

    print(response.status_code)
    print(json_result, file=sys.stdout)
    return json_result, image_data


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
            json_result, image_data = run_api(filename)
            current_app.logger.info(json_result, image_data)
            return render_template('plantid.html', data=json_result, image=image_data, email=session["email"])
    else:
        return render_template('upload.html', email=session["email"])
        #return render_template('plantid.html', data=json_result, image=image_data)


