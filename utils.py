import gi
gi.require_version('Gtk', '2.0')
from gi.repository import Gtk
import datetime

import os

def find_battery_name(search_path="/sys/class/power_supply/"):
	batteries = [b for b in os.listdir(search_path) if b.startswith("BAT")]
	if len(batteries) == 0:
		return None
	else:
		return batteries[0]

def get_save_file(current_folder=".", prefix="", extension=""):
	dialog = Gtk.FileChooserDialog(
		"Please choose a file", None,
		Gtk.FileChooserAction.SAVE,
		(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
	)

	# enable overwrite confirmation
	dialog.set_do_overwrite_confirmation(True)

	# set starting directory
	dialog.set_current_folder(current_folder)
	dialog.set_current_name(prefix + str(datetime.datetime.now()) + extension)

	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		return dialog.get_filename()
	elif response == Gtk.ResponseType.CANCEL:
		return None
