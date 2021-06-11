# COMMAND LINE INTERFACE CLASS

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
		pass