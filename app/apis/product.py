from math import ceil
from slugify import slugify
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import and_, or_
from pospax import db
from app.models import Product
from app.schema import ProductSchema

product_api = Blueprint('product_api', __name__, url_prefix='/api/product')
productSchema = ProductSchema(many=True)


@product_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@product_api.route('/list')
def product_list():
	products = Product.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y').all()
	return jsonify({
		'products': productSchema.dump(products).data
	})


@product_api.route('/get', defaults={'id': ''})
@product_api.route('/get/<id>')
def product_get(id):
	if id:
		product = Product.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y', id=id).first()
	else:
		no = db.session.query(db.func.max(Product.no)).filter_by(site_id=g.sid, branch_id=g.bid).scalar() or 0
		no = no + 1
		product = Product(site_id=g.sid, branch_id=g.bid)
		product.no = no
		product.code = 'P' + str(no).zfill(4)
	schema = ProductSchema()
	return jsonify({
		'product': schema.dump(product).data
	})


@product_api.route('/delete/<id>')
def product_delete(id):
	result = 0
	product = Product.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	if product:
		result = product.id
		if product.is_active == 'N':
			db.session.delete(product)
		else:
			product.is_active = 'N'
			db.session.merge(product)
		db.session.commit()
	return jsonify({ 'result': result })


@product_api.route('/save', methods=['POST'])
def product_save():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	forms = {
		'site_id': g.sid,
		'branch_id': g.bid,
		'no': f.get('no') or 0,
		'code': f.get('code') or '',
		'name': f.get('name') or '',
		'slug': slugify(f.get('name') or ''),
		'description_lc': f.get('description_lc') or '',
		'description_fg': f.get('description_fg') or '',
		'cate_id': f.get('cate_id') or None,
		'unit_price': f.get('unit_price') or 0,
		'cost_price': f.get('cost_price') or 0,
		'img': f.get('img') or None,
		'img_path': f.get('img_path') or None,
		'is_hot': 'Y' if (f.get('is_hot') or '') == 'on' else 'N',
		'is_visible': 'Y' if (f.get('is_visible') or '') == 'on' else 'N'
	}

	id = f.get('id') or None
	if id:
		product = Product.query.get(id)
		for k, v in forms.iteritems():
			setattr(product, k, v)
		db.session.merge(product)
	else:
		product = Product()
		for k, v in forms.iteritems():
			setattr(product, k, v)
		db.session.add(product)
	db.session.commit()

	if product: result = product.id
	return jsonify({ 'result': result })


@product_api.route('/search', methods=['POST'])
def product_search():
	products = []
	f = request.get_json()
	if f is None:
		f = request.form

	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	sort = f.get('sort') or None
	desc = f.get('desc') or False
	active = f.get('is_active') or 'Y'
	cate_id = f.get('cate_id') or None

	query = Product.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active=active)
	if term:
		query = query.filter(or_(
			Product.code.ilike('%' + term + '%'),
			Product.name.ilike('%' + term + '%'),
			Product.description_lc.ilike('%' + term + '%'),
			Product.description_fg.ilike('%' + term + '%'),
		))

	if cate_id:
		query = query.filter_by(cate_id=cate_id)

	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total

	if sort:
		query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

	products = query.limit(rp).offset((page - 1) * rp)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'products': productSchema.dump(products).data
	})


@product_api.route('/term', methods=['POST'])
def product_term():
	products = []
	f = request.get_json()
	if f is None:
		f = request.form

	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	cate_id = f.get('cate_id') or ''
	query = Product.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y')
	if cate_id:
		query = query.filter_by(cate_id=cate_id)

	if term:
		query = query.filter(or_(
			Product.code.ilike('%' + term + '%'),
			Product.name.ilike('%' + term + '%'),
			Product.description.ilike('%' + term + '%'),
		))

	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total
	products = query.limit(rp).offset((page - 1) * rp)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'products': productSchema.dump(products).data
	})
