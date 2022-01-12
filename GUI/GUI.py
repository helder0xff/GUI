import tkinter as tk
from tkinter import messagebox
import json

class GUI:
	def __init__(self, configFile, size = "512x512", callback  = ''):
		self.__data = { }
		self.__stringvars = { }
		self.__entries = { }
		self.__yPlacement = 0

		self.__callback = callback
		config = self.__parseConfigFile(configFile)
		self.__main_menu = config['main_menu']
		self.__dropddown_entries = config['dropdown_entries']
		self.__help_message = self.__joinStringArray(config['help_message'])

		self.__root = tk.Tk()
		self.__root.geometry(size)
		self.__root.title('Exmperiment Configurator')
		self.__root.configure()
		self.__layoutMenu()
		self.__root.mainloop()

	def __joinStringArray(self, stringArray):
		jointString = ''
		for string in stringArray:
			jointString += (string + '\n')

		return jointString

	def __parseConfigFile(self, configFile):
		file = open(configFile)
		config = json.load(file)
		file.close()

		return config

	def __increment_yPlacement(self, increment = 25):
		self.__yPlacement += increment

	def __parseDropDownFromDict(self, dictionary, dropDownKey):
		parsedDropDown = {}
		for key in dictionary:
			if dropDownKey in key:
				if None != dictionary[dropDownKey]:
					if '_' not in key:
						parsedDropDown['type'] = dictionary[dropDownKey]
					else:
						underscorIndex = key.rfind('_')
						rippedKey = key[underscorIndex + 1:]
						parsedDropDown[rippedKey] = dictionary[key]

		return parsedDropDown

	def __parseData(self):
		parsedData = {}
		entryKeys = []
		dropDownKeys = []
		for key in self.__main_menu:
			itemClass = self.__main_menu[key]['class']
			if 'entry' == itemClass:
				entryKeys.append(key)
			elif 'dropdown'== itemClass:
				dropDownKeys.append(key)

		for key in dropDownKeys:
			parsedDropDown = self.__parseDropDownFromDict(self.__data, key)
			if {} != parsedDropDown:
				parsedData[key] = parsedDropDown

		for key in entryKeys:
			if None != self.__data[key]:
				parsedData[key] = self.__data[key]

		return parsedData

	def getData(self):
		return self.__parseData()

	def __resetButton(self):
		button = tk.Button(self.__root,
							text = 'Reset',
							command = self.__resetCallback)
		self.__increment_yPlacement()
		button.place(x = 0, y = self.__yPlacement)

	def __resetCallback(self):
		entriesCopy = self.__entries.copy()
		for key in entriesCopy:
			self.__destroyEntry(key)
		for key in self.__main_menu:
			if 'entry' == self.__main_menu[ key ][ 'class' ]:
				self.__createEntry(key)

	def __runButton(self):
		button = tk.Button(self.__root,
							text = 'Run',
							command = self.__runCallback)
		self.__increment_yPlacement()
		button.place(x = 0, y = self.__yPlacement)

	def __runCallback(self):
		self.__getDataFromMenu()
		self.__root.destroy()
		self.__callback()

	def __getDataFromMenu(self):
		for key in self.__stringvars:
			self.__data[ key ] = self.__stringvars[ key ].get()
			self.__data[ key ] = self.__data[ key ] if self.__data[ key ] != 'None' else None
		for key in self.__entries:
			self.__data[ key ] = self.__entries[ key ][ 'entry' ].get()
			self.__data[ key ] = int(self.__data[ key ]) if self.__data[ key ] != '' else None

	def __helpButton(self):
		button = tk.Button(self.__root,
		                    text = 'Help',
		                    command = self.__helpCallback)
		self.__increment_yPlacement()
		button.place(x = 0, y = self.__yPlacement)

	def __helpCallback(self):
	    box = messagebox.showinfo('help', self.__help_message)

	def __layoutMenu(self):
		self.__runButton()
		self.__helpButton()
		self.__resetButton()
		for key in self.__main_menu:
			if 'entry' == self.__main_menu[ key ][ 'class' ]:
				self.__createEntry(key)
			if 'dropdown' == self.__main_menu[ key ][ 'class' ]:
				self.__createDropdown(self.__main_menu[ key ][ 'choices' ], key)

	def __createEntry(self, name):
		if name not in self.__entries:
		    entry = tk.Entry(self.__root)
		    entry.pack()
		    label = tk.Label(self.__root, text = name)
		    label.pack()		    
		    self.__entries[ name ] = { 'label': label, 'entry': entry }

	def __destroyEntry(self, name):
		if name in self.__entries:
		    self.__entries[ name ][ 'label' ].destroy()
		    self.__entries[ name ][ 'entry' ].destroy()
		    self.__entries.pop(name)

	def __createDropdown(self, choices, name):
		label = tk.Label(self.__root, text = name)
		self.__increment_yPlacement(50)
		label.place(x = 0, y = self.__yPlacement)
		var = tk.StringVar(name = name, value = 'None')
		menu = tk.OptionMenu(  self.__root,
		                        var,
		                        *choices,
		                        command = self.__dropdownCallback)
		self.__increment_yPlacement()
		menu.place(x = 0, y = self.__yPlacement)
		self.__stringvars[ name ] = var

	def __dropdownCallback(self, choice):
		for entry in self.__dropddown_entries[ choice ]:
			for key in self.__stringvars:
				if self.__stringvars[ key ].get() == choice:
					for entry in self.__dropddown_entries[ choice ]:
						self.__createEntry(key + '_' + entry)

#### end of life #####
