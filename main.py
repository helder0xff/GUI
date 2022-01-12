from GUI.GUI import GUI

def function():
	print("I am a callback.")

def main():
	gui = GUI('GUI_config.json', callback = function)
	print(gui.getData())

main()


#### end of file ####