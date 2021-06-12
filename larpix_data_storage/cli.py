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

		self.tile_arr = []


	def display_menu(self):
		print('\n')
		print("Welcome to the UTA LArPix QC Testing Database, choose an option...")
		print("(1) Add a new tile to the database") # input serial number -> initialize chips, uarts, and configs
		print("(2) Display all tiles saved to the database")
		print("(q) Save and exit program")
		print('\n')


	def add_tile(self):
		tile_input = str(input("Enter a tile serial number (000, 001, 002, etc...) or quit (q): ")).lower()
		if tile_input == 'q': pass
		else:
			try:
				tile = Tile(tile_input)
				print("Data found for: {}".format(tile))
				print("Adding tile to database...")
				self.tile_arr.append(tile)
			except:
				pass


	def display_all_tiles(self):
		for tile in self.tile_arr: print("{}".format(tile))


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
			elif menu_input == '2':
				self.display_all_tiles()
				continue
			else:
				print("Not an acceptable input! Try again!")
				continue


if __name__ == "__main__":
	interface = CLI()
	interface.run()
