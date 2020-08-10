import eel
@eel.expose

def hello():
	print('Hello World!')

eel.init('www')
eel.start('index.html')