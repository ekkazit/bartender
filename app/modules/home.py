from flask import Blueprint, render_template, request, g
from pospax import db
from app.models import Bill, Status

home_app = Blueprint('home_app', __name__, url_prefix='/home')


@home_app.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@home_app.route('/')
def home_index():
	status = Status.query.filter_by(name='new', module='bill').first()
	bill_count = db.session.query(db.func.count(Bill.no)).filter_by(
		site_id=g.sid, branch_id=g.bid, status_id=status.id).scalar() or 0
	return render_template('home.html', bill_count=bill_count)
