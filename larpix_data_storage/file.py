# FILE CLASS

# maybe implement as instances 
# (File uart_file, File config_file, File larpix_file, etc...)
# within respective classes

import json

class File:
	'''
	METHODS:
	ATTRIBUTES:
		- tile serial number
		- filetype conditional list to keep track of the path used 
			- <[uart_file, config_file, larpix_file]>
	'''
	PATH = '/Users/jamesdeleon/Documents/larpix/larpix_v3_4_0/UTA_plotting_scripts/larpix_data_storage/test_data/'

	def __init__(self, serial_num, filetype = [False, False, False]):
		self.serial_num = str(serial_num)
		self.filetype = filetype

		if self.filetype == [True, False, False]: self.path = File.PATH + self.serial_num + '/uart.json'		# uart path
		elif self.filetype == [False, True, False]: self.path = File.PATH + self.serial_num + '/configs_dir/'	# config path
		elif self.filetype == [False, False, True]: self.path = File.PATH + 'data.json'							# larpix path
		else: self.path = "No existing path found with these conditions!"

	def open_file(self):
		try:
			with open(self.path, 'r') as file:
				data = json.load(file)
			file.close()
		except: data = "No data found!"
		finally: return data

	def save_file(self):
		pass

	def copy_file(self):
		pass


if __name__ == "__main__":
	pass