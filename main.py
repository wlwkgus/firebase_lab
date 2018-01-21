from flask import Flask, render_template, Response
from time import sleep

# socket io import
from flask import session
from flask_socketio import SocketIO, emit

# pyrebase wrapper
from firebase import firebase_db

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--stage', type=int, default=0, help='')
opt = parser.parse_args()
template_folder = None

if opt.stage == 0:
	template_folder = '0/'
elif opt.stage == 1:
	template_folder = '1/'
elif opt.stage == 2:
	template_folder = '2/'
elif opt.stage == 3:
	pass

if template_folder:
	app = Flask(__name__, template_folder=template_folder)
else:
	app = Flask(__name__)
app.debug = True
app.host = '0.0.0.0'
app.port = 5000
socketio = SocketIO(app)

### chatting streamer
def chatting_stream_handler(data):
	print(data)
	# emit("chattings", data)

@app.route('/')
def index():
	chatting_stream = firebase_db.child("chattings").stream(chatting_stream_handler)
	chatting_stream.start()
	return render_template('chat.html')

### websocket section
@socketio.on('connect', namespace='/chattings')
def connect():
	emit("response", {'message': 'Connected'})

@socketio.on('disconnect', namespace='/chattings')
def disconnect():
	session.clear()
	print("Disconnected")

@socketio.on('request', namespace='/chattings')
def request(data):
	# TODO : validate given data.
	firebase_db.child('chattings').push({
		'username': data['username'],
		'message': data['message'],
		'hours': data['hours'],
		'minutes': data['minutes']
	})
	emit("response", {'is_success': True})


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    socketio.run(app)
