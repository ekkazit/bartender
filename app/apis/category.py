from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from pospax import db
from app.models import Category
from app.schema import CategorySchema

category_api = Blueprint('category_api', __name__, url_prefix='/api/category')
categorySchema = CategorySchema(many=True)


@category_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@category_api.route('/list')
def category_list():
	categories = Category.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y').all()
	return jsonify({
		'categories': categorySchema.dump(categories).data
	})


@category_api.route('/get', defaults={'id': ''})
@category_api.route('/get/<id>')
def category_get(id):
	category = Category(site_id=g.sid, branch_id=g.bid)
	if id:
		category = Category.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y', id=id).first()
	schema = CategorySchema()
	return jsonify({
		'category': schema.dump(category).data
	})


@category_api.route('/delete/<id>')
def category_delete(id):
	result = 0
	category = Category.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	if category:
		result = category.id
		if category.is_active == 'N':
			db.session.delete(category)
		else:
			category.is_active = 'N'
			db.session.merge(category)
		db.session.commit()
	return jsonify({ 'result': result })


@category_api.route('/save', methods=['POST'])
def category_save():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	forms = {
		'site_id': g.sid,
		'branch_id': g.bid,
		'name': f.get('name') or '',
		'description': f.get('description') or ''
	}

	id = f.get('id') or None
	if id:
		category = Category.query.get(id)
		for k, v in forms.iteritems():
			setattr(category, k, v)
		db.session.merge(category)
	else:
		category = Category()
		for k, v in forms.iteritems():
			setattr(category, k, v)
		db.session.add(category)
	db.session.commit()

	if category: result = category.id
	return jsonify({ 'result': result })


@category_api.route('/search', methods=['POST'])
def category_search():
	f = request.get_json()
	if f is None:
		f = request.form
	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	sort = f.get('sort') or None
	desc = f.get('desc') or False
	active = f.get('is_active') or 'Y'

	query = Category.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active=active)
	if term:
		query = query.filter(or_(
			Category.name.ilike('%' + term + '%'),
			Category.description.ilike('%' + term + '%'),
		))

	if sort:
		query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total

	categories = query.limit(rp).offset((page - 1) * rp)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'categories': categorySchema.dump(categories).data
	})
