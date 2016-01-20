from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from pospax import db
from app.models import Customer
from app.schema import CustomerSchema

customer_api = Blueprint('customer_api', __name__, url_prefix='/api/customer')
customerSchema = CustomerSchema(many=True)


@customer_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@customer_api.route('/list')
def customer_list():
	customers = Customer.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y').all()
	return jsonify({
		'customers': customerSchema.dump(customers).data
	})


@customer_api.route('/get', defaults={'id': ''})
@customer_api.route('/get/<id>')
def customer_get(id):
	if id:
		customer = Customer.query.filter_by(site_id=g.sid, branch_id=g.bid,is_active='Y', id=id).first()
	else:
		no = db.session.query(db.func.max(Customer.no)).filter_by(
			site_id=g.sid, branch_id=g.bid).scalar() or 0
		no = no + 1
		customer = Customer(site_id=g.sid, branch_id=g.bid)
		customer.no = no
		customer.code = 'C' + str(no).zfill(4)
	schema = CustomerSchema()
	return jsonify({
		'customer': schema.dump(customer).data
	})


@customer_api.route('/delete/<id>')
def customer_delete(id):
	result = 0
	customer = Customer.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	if customer:
		result = customer.id
		if customer.is_active == 'N':
			db.session.delete(customer)
		else:
			customer.is_active = 'N'
			db.session.merge(customer)
		db.session.commit()
	return jsonify({ 'result': result })


@customer_api.route('/add', methods=['POST'])
def customer_add():
	result = None
	f = request.get_json()
	if f['customer']: f = f['customer']
	forms = {
		'site_id': g.sid,
		'branch_id': g.bid,
		'firstname': f.get('firstname') or '',
		'lastname': f.get('lastname') or '',
		'gender': f.get('gender') or None,
		'email': f.get('email') or None,
		'phone': f.get('phone') or '',
		'img': f.get('img') or None,
		'img_path': f.get('img_path') or None
	}

	email = f.get('email') or ''
	cust = Customer.query.filter_by(site_id=g.sid, branch_id=g.bid, email=email).first()
	if cust:
		# customer already existed
		result = cust
	else:
		# save new customer
		customer = Customer(site_id=g.sid, branch_id=g.bid)
		for k, v in forms.iteritems():
			setattr(customer, k, v)
		if customer.code is None:
			no = db.session.query(db.func.max(Customer.no)).filter_by(
				site_id=g.sid, branch_id=g.bid).scalar() or 0
			no = no + 1
			customer.no = no
			customer.code = 'C' + str(no).zfill(4)
		db.session.add(customer)
		db.session.commit()
		result = customer
	# serializer for customer
	data = {}
	if result:
		schema = CustomerSchema()
		data = schema.dump(result).data
	return jsonify({ 'result': data })


@customer_api.route('/save', methods=['POST'])
def customer_save():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	forms = {
		'site_id': g.sid,
		'branch_id': g.bid,
		'no': f.get('no') or 0,
		'code': f.get('code') or '',
		'firstname': f.get('firstname') or '',
		'lastname': f.get('lastname') or '',
		'gender': f.get('gender') or None,
		'email': f.get('email') or None,
		'phone': f.get('phone') or '',
		'img': f.get('img') or None,
		'img_path': f.get('img_path') or None
	}

	id = f.get('id') or None
	if id:
		customer = Customer.query.get(id)
		for k, v in forms.iteritems():
			setattr(customer, k, v)
		db.session.merge(customer)
	else:
		customer = Customer()
		for k, v in forms.iteritems():
			setattr(customer, k, v)
		db.session.add(customer)
	db.session.commit()

	if customer: result = customer.id
	return jsonify({ 'result': result })


@customer_api.route('/search', methods=['POST'])
def customer_search():
	f = request.get_json()
	if f is None:
		f = request.form

	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	sort = f.get('sort') or None
	desc = f.get('desc') or False
	active = f.get('is_active') or 'Y'

	query = Customer.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active=active)
	if term:
		query = query.filter(or_(
			Customer.code.ilike('%' + term + '%'),
			Customer.email.ilike('%' + term + '%'),
			Customer.firstname.ilike('%' + term + '%'),
			Customer.lastname.ilike('%' + term + '%'),
		))

	if sort:
		query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total

	customers = query.limit(rp).offset((page - 1) * rp)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'customers': customerSchema.dump(customers).data
	})


@customer_api.route('/term', methods=['POST'])
def customer_term():
	f = request.get_json()
	if f is None:
		f = request.form
	term = f.get('q') or None
	query = Customer.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y')
	if term:
		query = query.filter(or_(
			Customer.code.ilike('%' + term + '%'),
			Customer.email.ilike('%' + term + '%'),
			Customer.firstname.ilike('%' + term + '%'),
			Customer.lastname.ilike('%' + term + '%'),
		))
	customers = query.all()
	return jsonify({
		'customers': customerSchema.dump(customers).data
	})
