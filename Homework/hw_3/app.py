from flask import Flask, render_template, request
import json

app = Flask(__name__)

# 
# {
#     "Something username": {
#         "name": "Something name",
#         "password": "Somthing password"
#     }
# }
#
# *only one user for one operation
@app.route("/registration", methods=["POST"])
def registration():
    newData = request.json

    with open("data.json", "r") as file:
        data = json.load(file)

    for key, value in newData.items():
        if(key not in data):
            data[key] = value
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            return "Register complited"
        else:
            return "Currect username is used"
#
# {
#     "Something username": {
#         "password": "Something password"
#     }
# }
#
@app.route("/verify", methods=["POST"])
def verify():
    loginData = request.json

    with open("data.json", "r") as file:
        data = json.load(file)
    
    for key, value in loginData.items():
        if(key in data):
            if(value['password'] == data[key]['password']):
                return "Login complited"
            return "Uncorrect password"
        else:
            return "Unknow user"
#
# {
#     "Something username": {
#         "password": "Something password"
#         "new_password" : "Something new password"
#     }
# }
#
@app.route("/change_password", methods=["PUT"])
def change_password():
    changedData = request.json

    with open("data.json", "r") as file:
        data = json.load(file)

    for key, value in changedData.items():
        if(key in data):
            if(value['password'] == data[key]['password']):
                data[key]['password'] = value['new_password']
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                return "Password changed"
            return "Uncorrect password"
        else:
            return "Unknow user"

#
# {
#     "Something username": {
#         "password": "Something password"
#     }
# }
#
@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    changedData = request.json

    with open("data.json", "r") as file:
        data = json.load(file)

    for key, value in changedData.items():
        if(key in data):
            if(value['password'] == data[key]['password']):
                del data[key]
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                return "User deleted"
            return "Uncorrect password"
        else:
            return "Unknow user"


@app.route("/get_all_users", methods=["GET"])
def get_all_users():
    with open("data.json", "r") as file:
        data = json.load(file)

    return data

if(__name__ == "__main__"):
    app.run(debug=True)
