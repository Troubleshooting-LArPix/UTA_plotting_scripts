# CHIP CLASS

from file import File

class Chip:
	'''
	METHODS:
		- ability to parse a config file

	ATTRIBUTES:
		- config file
		- chip ID (io group, io channel, chip id)
	'''
	def __init__(self, serial_num, io_group, io_channel, chip_id):
		self.serial_num = str(serial_num)
		self.io_group = str(io_group)
		self.io_channel = str(io_channel)
		self.chip_id = str(chip_id)

		self.config_dir = File(self.serial_num, [False, True, False])
		self.config_file = self.find_config_file()
		self.config_data = self.config_dir.open_file(self.config_file)


	def __str__(self):
		return "Chip: {0}-{1}-{2}".format(self.io_group, self.io_channel, self.chip_id)


	def __eq__(self, chip):
		return (chip.io_group == self.io_group) and (chip.io_channel == self.io_channel) and (chip.chip_id == self.chip_id) 


	def find_config_file(self):
		for file in self.config_dir.config_files:
			io_group = file.split('-')[1]
			io_channel = file.split('-')[2]
			chip_id = file.split('-')[3]

			if (io_group == self.io_group) and (io_channel == self.io_channel) and (chip_id == self.chip_id):
				file_ext = file.split('/')[-1]
				return file_ext
		return "No config file found for this chip!"


if __name__ == "__main__":
	chips = [Chip('000',1,1,11), Chip('000',1,1,12), Chip('000',1,1,13)]

	for chip in chips: print("{}".format(chip))
	print('\n')
	
	for chip in range(0, len(chips)): print("{}\n".format(chips[chip].config_data))
