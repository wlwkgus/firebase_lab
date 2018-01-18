from flask import Flask, render_template
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

@app.route('/')
def index():
	return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
