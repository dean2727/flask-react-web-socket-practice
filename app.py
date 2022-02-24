from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
from flask_cors import cross_origin

app = Flask(__name__)
app.secret_key = "hello"

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

# users model for our database, similar to Django but more native to python
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # varchar
    email = db.Column(db.String(100))
    
    # constructor called when we create a new model object
    def __init__(self, name, email):
        self.name = name
        self.email = email

socketIo = SocketIO(app, cors_allowed_origins="*")

# by setting this to true, we dont need to start the server manually when we change the code
app.debug = True

app.host = 'localhost'

@cross_origin
@socketIo.on("message")
def handleMessage(msg):
    print(msg)
    # send() sends a standard message of string or JSON to the client
    # emit() sends a message under a custom application-defined event name
    # When a message is sent with the broadcast option enabled, all clients connected to the namespace receive it, including the sender
    send(msg, broadcast=True)
    return None

@cross_origin
@socketIo.on("connect")
def handle_connection():
    print("a user has connected")
    send("Hello partner!", broadcast=True)

@cross_origin
@app.route("/", methods=['GET'])
def getDummyData():
    return jsonify(success=True)

if __name__ == "__main__": 
    # create the database if it doesnt exist already, before running
    db.create_all()
    
    socketIo.run(app)