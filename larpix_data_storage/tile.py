# TILE CLASS

from chip import Chip
from file import File

class Tile:
	'''
	METHODS:
		- ability to pull up and assign configs for each chip
		- ability to assign uart path to tile
		- ability to differentiate between cold and warm tests
		- creates 100 Chip objects with a chip ID, gives each Chip object a config file
		- ability to automatically assign a chip id to each chip based on the uart path
		
		- this class stores the data, it should parse through each config dir with a matching serial number

	ATTRIBUTES:
		- serial number
		- file object for the uart file path/data
		- cryo or non-cryo state
		- a list of 100 Chip objects
	'''
	def __init__(self, serial_num):
		self.serial_num = str(serial_num)

		self.uart_file = File(self.serial_num, [True, False, False])
		self.uart_data = self.uart_file.open_file()

		self.chips = []
		self.initialize_chips()


	def __str__(self):
		return "Tile: {0}".format(self.serial_num)


	def initialize_chips(self):
		for io_channel in range(1, 5):
			for chip in self.uart_data['network']['1'][str(io_channel)]['nodes']:
				if not chip['chip_id'] == 'ext': self.chips.append(Chip(self.serial_num, 1, io_channel, chip['chip_id']))


if __name__ == "__main__":
	while True:
		tile_input = str(input("Enter a tile serial number (000, 001, 002), or quit (q): ")).lower()
		if tile_input == 'q': break
		else:
			tile_test = Tile(tile_input)
			print("{}".format(tile_test))
			for chip in tile_test.chips: print("Data initialized for: {}".format(chip))

			while True:
				chip_input = str(input("Enter a chip id to see config information (1-1-11), or quit (q): ")).lower()
				if chip_input == 'q': break
				else:
					try:
						io_group = chip_input.split('-')[0]
						io_channel = chip_input.split('-')[1]
						chip_id = chip_input.split('-')[2]
						for chip in tile_test.chips:
							if chip.io_group == io_group and chip.io_channel == io_channel and chip.chip_id == chip_id:
								print("{}\n".format(chip.config_data))
					except:
						print("Input chip configuration not recognized!")
