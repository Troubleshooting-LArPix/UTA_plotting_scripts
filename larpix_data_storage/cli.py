# COMMAND LINE INTERFACE CLASS

# do enough to create a data.json file from scatch with the current test data

import json
import glob
from file import File
from chip import Chip
from tile import Tile

class CLI:
	'''
	METHODS:
		- ability to display a tile's initialized chips
		- ability to display a tile's uart path
		- ability to display a chip's config data
		- ability to display a chip's config file path

		- ability to add a new tile by inputting serial number
		- ability to add a new uart path to the tile
		- ability to save all data when program is going inactive (.larpix ext)
		- ability to copy all data onto a <file1>.larpix backup
		- ability to open all data when program is going active (.larpix ext)
		- ability to change a tile's info/ chip's info (more advanced method)

	ATTRIBUTES:
		- a menu showing a user which actions to perform
	'''
	def __init__(self):
		print("Initializing interface...")
		self.init_file = File('', [False, False, True])
		self.init_data = self.init_file.open_file()
		print("Interface initialized!")


	def display_menu(self):
		print("Welcome to the LArPix Database, choose an option...")
		print("(1) Add a new tile to the database") # input serial number, initialize chips, uarts, and configs
		print("(q) Save and exit program")
		print('\n')


	def add_tile(self):
		pass


	def save(self):
		pass


	def run(self):
		while True:
			self.display_menu()
			menu_input = str(input("Enter an option: ")).lower()

			if menu_input == 'q':
				self.save()
				break
			elif menu_input == '1':
				self.add_tile()
				continue
			else:
				print("Not an acceptable input! Try again!")
				continue


if __name__ == "__main__":
	interface = CLI()
	interface.run()

