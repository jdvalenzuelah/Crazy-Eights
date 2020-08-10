import eel

@eel.expose

def hello():
	print('Hello World!')

eel.init('www')
eel.start('example.html')
#https://github.com/BradySheehan/Crazy_Eights_live/blob/master/crazy_eights/Crazy8_2.html