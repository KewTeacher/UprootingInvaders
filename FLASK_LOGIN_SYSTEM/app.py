
from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://apple123:<password>@cluster0.fba3n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('total_records')
records = db.registe`