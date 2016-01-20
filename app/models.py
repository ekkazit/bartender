from pospax import db

class Base(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
	updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp())


class Role(Base):
	__tablename__ = 'roles'
	name = db.Column(db.String(20))
	description = db.Column(db.String(50), nullable=True)
	is_active = db.Column(db.String(1), default='Y')
	users = db.relationship('User', backref='roles', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Role, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'roles %r' % self.name


class Status(Base):
	__tablename__ = 'status'
	name = db.Column(db.String(20))
	module = db.Column(db.String(20))
	description = db.Column(db.String(50), nullable=True)
	is_active = db.Column(db.String(1), default='Y')
	bills = db.relationship('Bill', backref='status', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Status, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'status %r' % self.name


class Site(Base):
	__tablename__ = 'sites'
	name = db.Column(db.String(50))
	company = db.Column(db.String(100), nullable=True)
	img = db.Column(db.String(50), nullable=True)
	img_path = db.Column(db.String(100), nullable=True)
	is_active = db.Column(db.String(1), default='Y')

	def __init__(self, *args, **kwargs):
		super(Site, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'sites %r' % self.name


class Branch(Base):
	__tablename__ = 'branch'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	no = db.Column(db.Integer)
	code = db.Column(db.String(10))
	name = db.Column(db.String(50))
	address = db.Column(db.String(100), nullable=True)
	phone = db.Column(db.String(20), nullable=True)
	fax = db.Column(db.String(20), nullable=True)
	email = db.Column(db.String(50), nullable=True)
	contact = db.Column(db.String(50), nullable=True)
	is_main = db.Column(db.String(1), default='N')
	is_active = db.Column(db.String(1), default='Y')

	def __init__(self, *args, **kwargs):
		super(Branch, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'branch %r' % self.name


class User(Base):
	__tablename__ = 'users'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	no = db.Column(db.Integer)
	code = db.Column(db.String(10))
	username = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(30))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	firstname = db.Column(db.String(50))
	lastname = db.Column(db.String(100), nullable=True)
	gender = db.Column(db.String(1), nullable=True)
	phone = db.Column(db.String(20), nullable=True)
	email = db.Column(db.String(50), nullable=True)
	img = db.Column(db.String(50), nullable=True)
	img_path = db.Column(db.String(100), nullable=True)
	is_active = db.Column(db.String(1), default='Y')
	bills = db.relationship('Bill', backref='users', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'users %r' % self.email


class Customer(Base):
	__tablename__ = 'customer'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	no = db.Column(db.Integer)
	code = db.Column(db.String(10))
	firstname = db.Column(db.String(50))
	lastname = db.Column(db.String(100), nullable=True)
	gender = db.Column(db.String(1), nullable=True)
	phone = db.Column(db.String(20), nullable=True)
	email = db.Column(db.String(50), nullable=True)
	img = db.Column(db.String(50), nullable=True)
	img_path = db.Column(db.String(100), nullable=True)
	is_active = db.Column(db.String(1), default='Y')
	bills = db.relationship('Bill', backref='customer', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Customer, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'customer %r' % self.email


class Table(Base):
	__tablename__ = 'tables'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	name = db.Column(db.String(30))
	description = db.Column(db.String(50), nullable=True)
	floor = db.Column(db.String(10), nullable=True)
	seats = db.Column(db.Integer, nullable=True)
	is_active = db.Column(db.String(1), default='Y')
	bills = db.relationship('Bill', backref='tables', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Table, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'tables %r' % self.name


class Category(Base):
	__tablename__ = 'category'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	name = db.Column(db.String(50))
	description = db.Column(db.String(50), nullable=True)
	is_active = db.Column(db.String(1), default='Y')
	products = db.relationship('Product', backref='category', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Category, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'category %r' % self.name


class Product(Base):
	__tablename__ = 'product'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	no = db.Column(db.Integer)
	code = db.Column(db.String(10))
	name = db.Column(db.String(50))
	description_lc = db.Column(db.String(100), nullable=True)
	description_fg = db.Column(db.String(100), nullable=True)
	cate_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	unit_price = db.Column(db.Float, default=0)
	cost_price = db.Column(db.Float, default=0)
	sale_price = db.Column(db.Float, default=0)
	slug = db.Column(db.String(50), nullable=True)
	img = db.Column(db.String(50), nullable=True)
	img_path = db.Column(db.String(100), nullable=True)
	is_visible = db.Column(db.String(1), default='N')
	is_hot = db.Column(db.String(1), default='N')
	is_feature = db.Column(db.String(1), default='N')
	is_active = db.Column(db.String(1), default='Y')
	bill_items = db.relationship('BillItem', backref='product', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Product, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'product %r' % self.name


class Bill(Base):
	__tablename__ = 'bill'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	no = db.Column(db.Integer)
	bill_no = db.Column(db.String(15))
	bill_date = db.Column(db.DateTime, default=db.func.current_timestamp())
	receipt_no = db.Column(db.String(15), nullable=True)
	tax_rate = db.Column(db.Float, default=0)
	discount_rate = db.Column(db.Float, default=0)
	currency = db.Column(db.String(5), nullable=True)
	total_qty = db.Column(db.Integer, default=0)
	total_price = db.Column(db.Float, default=0)
	total_tax = db.Column(db.Float, default=0)
	total_discount = db.Column(db.Float, default=0)
	total_amount = db.Column(db.Float, default=0)
	remark = db.Column(db.String(50), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
	table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=True)
	status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
	bill_items = db.relationship('BillItem', backref='bill', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(Bill, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'bill %r' % self.bill_no


class BillItem(Base):
	__tablename__ = 'bill_items'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
	line_no = db.Column(db.Integer)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	qty = db.Column(db.Integer, default=0)
	price = db.Column(db.Float, default=0)
	tax = db.Column(db.Float, default=0)
	discount = db.Column(db.Float, default=0)
	amount = db.Column(db.Float, default=0)
	remark = db.Column(db.String(50), nullable=True)

	def __init__(self, *args, **kwargs):
		super(BillItem, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'bill_items %r' % self.line_no


class Receipt(Base):
	__tablename__ = 'receipt'
	site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
	no = db.Column(db.Integer)
	receipt_no = db.Column(db.String(15))
	receipt_date = db.Column(db.DateTime, default=db.func.current_timestamp())
	method = db.Column(db.String(20), nullable=True)
	total_amount = db.Column(db.Float, default=0)
	total_charge = db.Column(db.Float, default=0)
	total_return = db.Column(db.Float, default=0)
	card_no = db.Column(db.String(20), nullable=True)
	card_issue = db.Column(db.String(50), nullable=True)

	def __init__(self, *args, **kwargs):
		super(Receipt, self).__init__(*args, **kwargs)

	def __repr__(self):
		return 'receipt %r' % self.receipt_no
