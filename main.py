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
	# Flask needs request context.
	with app.test_request_context('/chattings'):
		socketio.emit("chattings", data, namespace='/chattings', broadcast=False)


@app.route('/')
def index():
	return render_template('chat.html')

### websocket section
@socketio.on('connect', namespace='/chattings')
def connect():
	emit("response", {'message': 'Connected'})

@socketio.on('disconnect', namespace='/chattings')
def disconnect():
	session.clear()
	print("Disconnected")

@socketio.on('request_chattings', namespace='/chattings')
def request_chattings(data):
	chatting_stream = firebase_db.child("chattings").stream(chatting_stream_handler)

@socketio.on('send_chatting', namespace='/chattings')
def send_chatting(data):
	# TODO : validate given data.
	firebase_db.child('chattings').push({
		'username': data['username'],
		'message': data['message'],
		'hours': data['hours'],
		'minutes': data['minutes']
	})
	# if '쌍욕' in data['message']:
	# 	firebase_db.child('chattings').push({
	# 		'username': '관리자',
	# 		'message': '욕하지마세요 ^^',
	# 		'hours': data['hours'],
	# 		'minutes': data['minutes']
	# 	})
	emit("response", {'is_success': True})


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    socketio.run(app)
