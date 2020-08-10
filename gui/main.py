import eel
@eel.expose

def hello():
	print('Hello World!')

eel.init('gui/Interface')
eel.start('index.html')