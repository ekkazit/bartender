from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from pospax import db
from app.models import User
from app.schema import UserSchema

user_api = Blueprint('user_api', __name__, url_prefix='/api/user')
userSchema = UserSchema(many=True)


@user_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@user_api.route('/list')
def user_list():
	users = User.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y').all()
	return jsonify({
		'users': userSchema.dump(users).data
	})


@user_api.route('/get', defaults={'id': ''})
@user_api.route('/get/<id>')
def user_get(id):
	if id:
		user = User.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y', id=id).first()
	else:
		no = db.session.query(db.func.max(User.no)).filter_by(site_id=g.sid, branch_id=g.bid).scalar() or 0
		no = no + 1
		user = User(site_id=g.sid, branch_id=g.bid)
		user.no = no
		user.code = 'C' + str(no).zfill(4)
	schema = UserSchema()
	return jsonify({
		'user': schema.dump(user).data
	})


@user_api.route('/delete/<id>')
def user_delete(id):
	result = 0
	user = User.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y', id=id).first()
	if user:
		result = user.id
		if user.is_active == 'N':
			db.session.delete(user)
		else:
			user.is_active = 'N'
			db.session.merge(user)
		db.session.commit()
	return jsonify({ 'result': result })


@user_api.route('/save', methods=['POST'])
def user_save():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	forms = {
		'site_id': g.sid,
		'branch_id': g.bid,
		'username': f.get('username') or '',
		'password': f.get('password') or '',
		'code': f.get('code') or '',
		'role_id': f.get('role_id') or None,
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
		user = User.query.get(id)
		for k, v in forms.iteritems():
			setattr(user, k, v)
		db.session.merge(user)
	else:
		user = User()
		for k, v in forms.iteritems():
			setattr(user, k, v)
		db.session.add(user)
	db.session.commit()

	if user: result = user.id
	return jsonify({ 'result': result })


@user_api.route('/search', methods=['POST'])
def user_search():
	f = request.get_json()
	if f is None:
		f = request.form
	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	sort = f.get('sort') or None
	desc = f.get('desc') or False
	active = f.get('is_active') or 'Y'

	query = User.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active=active)
	if term:
		query = query.filter(or_(
			User.email.ilike('%' + term + '%'),
			User.firstname.ilike('%' + term + '%'),
			User.lastname.ilike('%' + term + '%'),
		))

	if sort:
		query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total

	users = query.limit(rp).offset((page - 1) * rp)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'users': userSchema.dump(users).data
	})
