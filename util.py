import os

def find_battery_name(search_path="/sys/class/power_supply/"):
	batteries = [b for b in os.listdir(search_path) if b.startswith("BAT")]
	if len(batteries) == 0:
		return None
	else:
		return batteries[0]

class Bind(object):
	''' Bind a simple python function to a key binding. '''
	qtile = object()

	def __init__(self, functor, *args, **kwargs):
		'''
			Construct a binding.

			All arguments and keyword arguments besides the function are passed to the bound function.

			If an argument is Bind.qtile it will be replaced with the qtile object before being passed to the bound function.
		'''
		self.__functor = functor
		self.__args    = args
		self.__kwargs  = kwargs

	@staticmethod
	def __arg(arg, qtile):
		''' Preprocess an argument. '''
		if arg is Bind.qtile: return qtile
		return arg

	@staticmethod
	def __process_args(qtile, args, kwargs):
		''' Preprocess arguments. '''
		return (
			[     Bind.__arg(x, qtile) for x        in args]
			{key: Bind.__arg(x, qtile) for (key, x) in kwargs.items()}
		)

	def check(self, qtile):
		# This is kind of a hack, implementing  the actual work in the check function.
		# However, it is the easiest way to do this without defning an actual command.
		args, kwargs = Bind.__process_args(qtile, self.__args, self.__kwargs)
		self.__functor(*args, **kwargs);
		os.sys.stdout.flush()

		# Return False to make sure the normal command handling isn't invoked.
		return False
