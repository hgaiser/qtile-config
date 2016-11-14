import os

def find_battery_name(search_path="/sys/class/power_supply/"):
	batteries = [b for b in os.listdir(search_path) if b.startswith("BAT")]
	if len(batteries) == 0:
		return None
	else:
		return batteries[0]
