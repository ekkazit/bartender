from app.models import *

def role_seeder():
	db.session.add(Role(name='Admin'))
	db.session.add(Role(name='Cashier'))
	db.session.add(Role(name='Staff'))
	db.session.commit()

def status_seeder():
	db.session.add(Status(name='new', module='bill'))
	db.session.add(Status(name='cancel', module='bill'))
	db.session.add(Status(name='delete', module='bill'))
	db.session.add(Status(name='paid', module='bill'))
	db.session.add(Status(name='complete', module='bill'))
	db.session.commit()

def sites_seeder():
	db.session.add(Site(name='Chill Cafe', company='Chill Cafe'))
	db.session.add(Site(name='Siam Restaurant', company='Siam Restaurant'))
	db.session.commit()

def branch_seeder():
	db.session.add(Branch(site_id=1, no=1, code='BH001', name='Chatuchak', is_main='Y', address='31/1 Navamin Road, Bangkhen, Bangkok 10500', phone='02-4458874', fax='02-8954785'))
	db.session.add(Branch(site_id=1, no=2, code='BH002', name='Kaset-Navamin'))
	db.session.add(Branch(site_id=1, no=3, code='BH003', name='Rachadalai Theatre'))
	db.session.commit()

def user_seeder():
	db.session.add(User(site_id=1, branch_id=1, no=1, code='U01', username='admin@mail.com', password='1', role_id=1, firstname='Sompop'))
	db.session.add(User(site_id=1, branch_id=1, no=2, code='U02', username='cashier@mail.com', password='1', role_id=2, firstname='Wirat'))
	db.session.add(User(site_id=1, branch_id=1, no=3, code='U03', username='staff@mail.com', password='1', role_id=3, firstname='Suchart'))
	db.session.commit()

def customer_seeder():
	db.session.add(Customer(site_id=1, branch_id=1, no=1, code='C01', firstname='Alex', email='alex@mail.com'))
	db.session.add(Customer(site_id=1, branch_id=1, no=2, code='C02', firstname='Mike', email='mile@mail.com'))
	db.session.add(Customer(site_id=1, branch_id=1, no=3, code='C03', firstname='Lorent', email='lorent@mail.com'))
	db.session.add(Customer(site_id=1, branch_id=1, no=4, code='C04', firstname='Yugene', email='yugene@mail.com'))
	db.session.add(Customer(site_id=1, branch_id=1, no=5, code='C05', firstname='Emma', email='emma@mail.com'))
	db.session.commit()

def category_seeder():
	db.session.add(Category(site_id=1, branch_id=1, name='Food'))
	db.session.add(Category(site_id=1, branch_id=1, name='Coffee'))
	db.session.add(Category(site_id=1, branch_id=1, name='Dessert'))
	db.session.commit()

def product_seeder():
	db.session.add(Product(site_id=1, branch_id=1, no=1, code='P01', name='Tuna Salad', cate_id=1, unit_price=100.00, img_path='/static/img/01.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=2, code='P02', name='Pizza Seafood', cate_id=1, unit_price=80.00, img_path='/static/img/02.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=3, code='P03', name='Pork Steak', cate_id=1, unit_price=50.00, img_path='/static/img/03.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=4, code='P04', name='Fried Rice', cate_id=1, unit_price=60.00, img_path='/static/img/04.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=5, code='P05', name='Hamburger', cate_id=1, unit_price=40.00, img_path='/static/img/05.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=6, code='P06', name='Espresso Iced', cate_id=2, unit_price=90.00, img_path='/static/img/06.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=7, code='P07', name='Caramel Machiato', cate_id=2, unit_price=70.00, img_path='/static/img/07.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=8, code='P08', name='Mocha Iced', cate_id=2, unit_price=150.00, img_path='/static/img/08.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=9, code='P09', name='Green Tea', cate_id=2, unit_price=80.00, img_path='/static/img/09.jpg'))
	db.session.add(Product(site_id=1, branch_id=1, no=10,code='P10', name='Cappucino Hot', cate_id=2, unit_price=140.00, img_path='/static/img/10.jpg'))
	db.session.commit()

def table_seeder():
	db.session.add(Table(site_id=1, branch_id=1, name='Table 1', seats=4))
	db.session.add(Table(site_id=1, branch_id=1, name='Table 2', seats=2))
	db.session.add(Table(site_id=1, branch_id=1, name='Table 3', seats=4))
	db.session.add(Table(site_id=1, branch_id=1, name='Table 4', seats=6))
	db.session.commit()

def bill_seeder():
	db.session.add(Bill(site_id=1, branch_id=1, no=1, bill_no='201501-00001', tax_rate=7, total_qty=2, total_amount=180, status_id=1, user_id=1, cust_id=1))
	db.session.add(Bill(site_id=1, branch_id=1, no=2, bill_no='201501-00002', tax_rate=7, total_qty=2, total_amount=110, status_id=1, user_id=2, table_id=1))
	db.session.commit()

def bill_item_seeder():
	db.session.add(BillItem(site_id=1, branch_id=1, bill_id=1, line_no=1, product_id=1, qty=1, price=100, amount=100))
	db.session.add(BillItem(site_id=1, branch_id=1, bill_id=1, line_no=2, product_id=2, qty=1, price=80, amount=80))
	db.session.add(BillItem(site_id=1, branch_id=1, bill_id=2, line_no=1, product_id=3, qty=1, price=50, amount=50))
	db.session.add(BillItem(site_id=1, branch_id=1, bill_id=2, line_no=2, product_id=4, qty=1, price=60, amount=60))
	db.session.commit()

def receipt_seeder():
	db.session.add(Receipt(site_id=1, branch_id=1, bill_id=1, no=1, receipt_no='R01', total_amount=180, total_charge=200, total_return=20))
	db.session.commit()

def generate_sample_data():
	role_seeder()
	status_seeder()
	sites_seeder()
	branch_seeder()
	user_seeder()
	customer_seeder()
	category_seeder()
	product_seeder()
	table_seeder()
	bill_seeder()
	bill_item_seeder()
	receipt_seeder()
	print 'All tables seeded'
