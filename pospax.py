from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)


@app.route('/public/<path:filename>')
def base_static(filename):
	return send_from_directory(app.root_path + '/public', filename)


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/signup')
def signup():
	return render_template('signup.html')


@app.route('/logout')
def logout():
	return render_template('logout.html')


@app.route('/keypad')
def keypad():
	return render_template('pos/keypad.html')


@app.route('/preview')
def preview():
	return render_template('preview.html')

from werkzeug.utils import import_string

for mod in app.config['BLUEPRINTS']:
	app.register_blueprint(import_string(mod))
