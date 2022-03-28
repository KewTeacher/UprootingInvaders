
from flask import Flask, Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import requests
import json
import os

# Blueprint Configuration
home = Blueprint(
    'home', __name__,
    template_folder='templates',
    static_folder='static'
)
#Uploading data stuff
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@home_bp.route('/upload', methods=['GET', 'POST'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
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
            #filename = secure_filename(file.filename)
            #global currentfilename
            #currentfilename = secure_filename(currentfilename)
            #filename = currentfilename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], currentfilename))
            return redirect(url_for('upload_file', name=currentfilename))
    return render_template("upload.html", data=json_result)


#API stuff
API_KEY = "2b10FP9NjPISdGPyjNBrQowG"	# Plant API_KEY here
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


def run_api(name):
    image_path = "uploads/"+ name
    image_data = open(image_path, 'rb')
    return image_path, image_data

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

    print(response.status_code)
    print(json_result)


def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

#Plant ID stuff
@app.route('/plantid', methods=['GET'])
def plantid():
     #   req = requests.get('https://cat-fact.herokuapp.com/facts')
     #   req = requests.Request('POST', url=api_endpoint, files=files, data=data)
         #datas = json.loads(req.results)
         global currentfilename
         run_api(currentfilename)
         return render_template('plantid.html', data=json_result, image=image_data)
