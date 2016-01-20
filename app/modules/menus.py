from flask import Blueprint, render_template, request, g

menu_app = Blueprint('menu_app', __name__, url_prefix='/menus')


@menu_app.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@menu_app.route('/')
def menus_index():
	return render_template('menus/index.html')


@menu_app.route('/keypad')
def menus_keypad():
	return render_template('menus/keypad.html')
