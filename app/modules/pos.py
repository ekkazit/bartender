from flask import Blueprint, render_template, request, g

pos_app = Blueprint('pos_app', __name__, url_prefix='/pos')


@pos_app.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@pos_app.route('/')
def pos_index():
	return render_template('pos/index.html')
