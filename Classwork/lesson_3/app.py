from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route("/")
def loadSite():
    with open("data.json") as file:
        data = json.load(file)
    return jsonify(data)

@app.route("/", methods=["POST"])
def addData():
    newData = request.json

    with open("data.json", "r") as file:
        data = json.load(file)

    data.append(newData)

    with open("data.json", "w") as file:
       json.dump(data, file, indent=4)

    return "Hello"


