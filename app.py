#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify, redirect, url_for
app = Flask(__name__)

with open("config.json", "r") as confRaw:
    conf = json.loads(confRaw.read())
    confRaw.close()
    confRaw = None

usersConnected = []
messages = [{'name': 'Server', 'message': "This is the start of the server"}]
@app.route('/')
def allMessages():
    return jsonify(messages)

@app.route('/join/<usrname>/')
def join(usrname):
    try:
        # Check if max allowed connected users reached. If not allow user to join
        if(len(usersConnected) >= conf["maxAllowedConnectedUsers"]):
            print("User Tried to join. Server is full :(")
            return jsonify({'error': "The server is full :( Sorry"})
        else:
            print(f"User {usrname} has joined the server")
            messages.append({
                "name": "Server",
                "message": f"User {usrname} has joined the server"
            })
            usersConnected.append(usrname)
    except Exception:
        return jsonify({'error': "Server Side Error: Try again later"})
    return redirect(url_for("update"))

@app.route("/ping/")
def ping():
    return jsonify({"status": "Running!!"})

@app.route('/send/<msgContent>/<usrname>/')
def send(msgContent, usrname):
    # First Validate the user
    for i in range(0, len(usersConnected)):
        if usrname == usersConnected[i]:
            # If the user has been connected through the /join/ gateway then send the message and stop validation
            print(f"{usrname}: {msgContent}")
            messages.append({
                "name": f"{usrname}",
                "message": f": {msgContent}"
            })
            return redirect(url_for("update"))
        elif not usrname == usersConnected[i] and i == len(usersConnected):
            # welp.. the user has not yet been connected through /join/..
            # is prob using the browser. 
            # How did they mess up using a super easy to understand OPEN SOURCED API.... 
            # smh
            print(f'<< WARNING>> Non-Validated User "{usrname}" tried to send {msgContent}, but we blocked it due to not being Validated')
            return jsonify({'error': "!! Not Validated !!"})

        else:
            # keep trying 
            # i guess
            pass
    

@app.route("/update/")
def update():
    return redirect(url_for("allMessages"))

            
app.run()