import urllib
import cStringIO
from functools import wraps, update_wrapper
from datetime import datetime
from flask import Blueprint, render_template, request, g, send_file, make_response, jsonify
from flask_mail import Message
from pospax import app, mail
from app.models import Branch, Bill

report_app = Blueprint('report_app', __name__, url_prefix='/report')
report_name_format = 'frameset?__report=bill.rptdesign&__format=pdf'

@report_app.before_request
def before_request():
	g.sid = 1
	g.bid = 1


def download_file(urls):
	temp_path = app.config['TEMP_PATH']
	dt = datetime.now()
	file_name = 'bill' + str(dt.microsecond) + '.pdf'
	full_upload_path = temp_path + file_name
	write_file(urls, full_upload_path)
	return file_name


def write_file(urls, full_upload_path):
	web = urllib.urlopen(urls)
	fs = open(full_upload_path, 'wb')
	fs.write(web.read())
	fs.close()
	web.close()


def nocache(view):
	@wraps(view)
	def no_cache(*args, **kwargs):
		response = make_response(view(*args, **kwargs))
		response.headers['Last-Modified'] = datetime.now()
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response
	return update_wrapper(no_cache, view)


@report_app.route('/bill/pdf/<id>')
@nocache
def bill_pdf(id):
	wfile = urllib.urlopen(app.config['REPORT_SERVER_URL'] + report_name_format + '&bill_id=' + id)
	return send_file(cStringIO.StringIO(wfile.read()), attachment_filename='file.pdf')


@report_app.route('/bill/email', methods=['GET', 'POST'])
def bill_email():
	f = request.get_json()
	if f is None:
		f = request.form

	id = f.get('bill_id') or None
	receiver = f.get('receiver') or None
	sender = f.get('sender') or 'admin@pospax.com'
	if id and receiver:
		pdfile = download_file(app.config['REPORT_SERVER_URL'] + report_name_format + '&bill_id=' + str(id))
		msg = Message(sender=sender, subject='Your bill receipt', recipients=[receiver])
		msg.body = 'You have got a receipt attached:'
		with app.open_resource('public/temp/' + pdfile) as fp:
			msg.attach(pdfile, 'application/pdf', fp.read())
		mail.send(msg)
		return jsonify({'result': 1})
	return jsonify({'result': 0})


@report_app.route('/dashboard')
def report_dashboard():
	return render_template('reports/dashboard.html')


@report_app.route('/sale')
def report_sale():
	branches = Branch.query.filter_by(site_id=g.sid).all()
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/sale.html',
		branches=branches, rpt_server=report_server, site_id=g.sid
	)


@report_app.route('/compare')
def report_compare():
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/compare.html',
		rpt_server=report_server, site_id=g.sid
	)


@report_app.route('/product')
def report_product():
	branches = Branch.query.filter_by(site_id=g.sid).all()
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/product.html',
		branches=branches, rpt_server=report_server, site_id=g.sid
	)


@report_app.route('/customer')
def report_customer():
	branches = Branch.query.filter_by(site_id=g.sid).all()
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/customer.html',
		branches=branches, rpt_server=report_server, site_id=g.sid
	)


@report_app.route('/bestseller')
def report_bestseller():
	branches = Branch.query.filter_by(site_id=g.sid).all()
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/bestseller.html',
		branches=branches, rpt_server=report_server, site_id=g.sid
	)


@report_app.route('/staff')
def report_staff():
	branches = Branch.query.filter_by(site_id=g.sid).all()
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/staff.html',
		branches=branches, rpt_server=report_server, site_id=g.sid
	)


@report_app.route('/orders', defaults={'id': ''})
@report_app.route('/orders/<id>')
def report_orders(id):
	branches = Branch.query.filter_by(site_id=g.sid).all()
	if id:
		bills = Bill.query.filter_by(site_id=g.sid, branch_id=id).all()
	else:
		bills = Bill.query.filter_by(site_id=g.sid).all()

	report_server = app.config['REPORT_SERVER_URL']
	return render_template('reports/orders.html',
		branches=branches, bills=bills, rpt_server=report_server, site_id=g.sid, id=int(id or '0')
	)
