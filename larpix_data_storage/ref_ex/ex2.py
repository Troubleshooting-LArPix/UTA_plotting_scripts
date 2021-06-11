# example class to see how initial arc parameters affect initialization

class EX2:
	def __init__(self, arg, state = False):
		self.arg = arg
		self.state = state

	def __str__(self):
		return "{}".format(self.state)


if __name__ == "__main__":
	object1 = EX2("Arg")
	print("State without initialization: {}".format(object1))

	object2 = EX2("Arg", True)
	print("State with initialization : {}".format(object2))
