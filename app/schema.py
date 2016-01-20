import re
from pospax import ma
from marshmallow import fields
from app.models import Role, Status, Site, Branch, User, Customer, Category, \
	Product, Table, BillItem, Bill, Receipt

def get_fields(Class, include=None, exclude=None):
	base = ['created_at', 'updated_at']
	if exclude:
		base += exclude
	cols =  [k for k in Class.__dict__.keys() if not k.startswith('_') and not k.endswith('_')]
	result_fields = list(set(cols) - set(base))
	if include:
		result_fields += include
	return result_fields


class BaseSchema(ma.Schema):
	description_untag = fields.Method('get_description_untag')
	def get_description_untag(self, object):
		if object.description:
			tags = re.compile(r'<[^>]+>')
			data = tags.sub('', object.description.replace('&nbsp;', ''))
			return (data[:100] + '..') if len(data) > 100 else data
		return ''


class RoleSchema(BaseSchema):
	class Meta:
		fields = get_fields(Role, exclude=['users'])


class StatusSchema(BaseSchema):
	class Meta:
		fields = get_fields(Status, exclude=['bills'])


class SiteSchema(BaseSchema):
	class Meta:
		fields = get_fields(Site)


class BranchSchema(BaseSchema):
	class Meta:
		fields = get_fields(Branch)


class UserSchema(BaseSchema):
	roles = fields.Nested(RoleSchema, only=('id', 'name'))
	class Meta:
		fields = get_fields(User, include=['roles'], exclude=['bills'])


class CustomerSchema(BaseSchema):
	class Meta:
		fields = get_fields(Customer, exclude=['bills'])


class TableSchema(BaseSchema):
	class Meta:
		fields = get_fields(Table, exclude=['bills'])


class CategorySchema(BaseSchema):
	class Meta:
		fields = get_fields(Category, exclude=['products'])


class ProductSchema(BaseSchema):
	category = fields.Nested(CategorySchema, only=('id', 'name'))
	class Meta:
		fields = get_fields(Product, include=['category'], exclude=['bill_items'])


class BillItemSchema(BaseSchema):
	product = fields.Nested(ProductSchema, only=('id', 'code', 'name', 'unit_price', 'img', 'img_path'))
	class Meta:
		fields = get_fields(BillItem, include=['product'])


class BillSchema(BaseSchema):
	bill_items = fields.Nested(BillItemSchema, many=True)
	status = fields.Nested(StatusSchema, only=('id', 'name', 'module'))
	tables = fields.Nested(StatusSchema, only=('id', 'name'))
	users = fields.Nested(UserSchema, only=('id', 'code', 'firstname', 'lastname', 'email', 'img', 'img_path'))
	customer = fields.Nested(UserSchema, only=('id', 'code', 'firstname', 'lastname', 'email', 'img', 'img_path'))
	class Meta:
		fields = get_fields(Bill, include=['users', 'customer', 'tables', 'status', 'bill_items'], exclude=['bill_items'])


class ReceiptSchema(BaseSchema):
	class Meta:
		fields = get_fields(Receipt)
