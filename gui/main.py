import eel
@eel.expose

def hello():
	print('Hello World!')

eel.init('Interface')
eel.start('index.html')