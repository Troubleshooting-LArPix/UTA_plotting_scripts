# FILE CLASS

# maybe implement as instances 
# (File uart_file, File config_file, File larpix_file, etc...)
# within respective classes

import json
import glob

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

		# UART PATH
		if self.filetype == [True, False, False]:
			self.path = File.PATH + self.serial_num + '/uart.json'

		# CONFIG PATH
		elif self.filetype == [False, True, False]:
			self.path = File.PATH + self.serial_num + '/configs_dir/'
			self.config_files = glob.glob(self.path + '*.json')

		# LARPIX PATH
		elif self.filetype == [False, False, True]:
			self.path = File.PATH + 'data.json'

		# UNKNOWN PATH
		else: 
			self.path = None


	def __str__(self):
		return "{}".format(self.path)


	def open_file(self, file_ext = ''):
		try:
			with open(self.path + file_ext, 'r') as file:
				data = json.load(file)
			file.close()
		except:
			data = None
			print("No data found!")
		finally:
			return data


	def save_file(self):
		pass


	def copy_file(self):
		pass


if __name__ == "__main__":
	test_uart_file = File("000", [True, False, False])
	test_config_dir = File("000", [False, True, False])

	print("Uart File: {}".format(test_uart_file))
	print("Data:\n{}".format(test_uart_file.open_file()))

	print('\n')

	print("Config Directory: {}".format(test_config_dir))
	print("Data:\n{}".format(test_config_dir.open_file("config-1-1-11-2021_04_28_14_35_CDT.json")))