from os import makedirs
from flask import Flask, render_template
import json

app = Flask(__name__)

with open("data.json") as file:
    dic = json.load(file)

@app.route("/")
def loadSite():
    return render_template("main.jinja", schedule=dic)
