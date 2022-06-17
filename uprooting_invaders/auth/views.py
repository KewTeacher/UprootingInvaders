from flask import Flask, flash, render_template, request, url_for, redirect, session, Blueprint
from flask.templating import render_template
from pprint import pprint
import requests
import json
from werkzeug.utils import secure_filename
import pymongo
import bcrypt
import os
import sys

# Blueprint Configuration
auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static'
)

auth.secret_key = "testing"
client = pymongo.MongoClient(""Mongo connection String Here", tlsInsecure=True)
#client = pymongo.MongoClient(os.getenv("DB_CONNECTION"))
db = client.get_database('uprooting_invaders')
records = db.register


@auth.route('/', methods = ['POST', 'GET'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("map.home"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            print(str(user_data), file=sys.stdout)

            return redirect(url_for("auth.login"))
            #return render_template('logged_in.html', email=new_email, user_data=str(user_data))
    return render_template('index.html')

#end of code to run it
if __name__ == "__main__":
    route.run(debug=True)


#Login in
@auth.route('/logged_in')
def logged_in():
    if "email" in session:
        #print(str(user_data), file=sys.stdout)
        print(str(session), file=sys.stdout)
        email = session["email"]
        return redirect(url_for("map.home"))
    else:
        return redirect(url_for("login"))


#More User Login information
@auth.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("map.home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                session["name"]= email_found['name']
                session['id']=str(email_found['_id'])
                print(session, file=sys.stdout)
                return redirect(url_for('map.home'))
            else:
                if "email" in session:
                    return redirect(url_for("map.home"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


#Logout
@auth.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        session.pop("id", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')
