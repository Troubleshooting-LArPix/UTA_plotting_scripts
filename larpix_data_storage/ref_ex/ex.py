# this example class is made to show that methods can be called from the constructor

class Ex:
	def __init__(self, length, width):
		self.length = length
		self.width = width
		self.area = self.get_area() # methods can be called in the constructor!

	def get_area(self):
		return self.length * self.width

	def __str__(self):
		return "Area: {}".format(self.area)

if __name__ == "__main__":
	ex = Ex(3, 5)
	print("{}".format(ex))

