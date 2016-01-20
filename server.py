from pospax import app

def runserver():
	app.run(threaded=True)

if __name__ == '__main__':
	runserver()
