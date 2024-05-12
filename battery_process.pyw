import os
import sys
import json

path = os.getcwd()
settings_file = os.path.join(path, "settings.json")

try:
	data = json.load(open(settings_file))
except Exception:
	print("'settings.json' file not found.")
	sys.exit(1)

BATTERY_HIGH_LEVEL = data["battery_high_level"]
BATTERY_LOW_LEVEL = data["battery_low_level"]

import psutil
from time import sleep
from winotify import Notification, audio

def notify(title, msg=""):
	toast = Notification(
		app_id = "Battery Notifier",
		title = title,
		msg= msg,
		# displaying time
		duration="short"
	)
	toast.set_audio(sound=audio.Mail, loop=False)
	return toast.show()


def show_notification():
	battery = psutil.sensors_battery()

	if battery.power_plugged:
		if battery.percent >= BATTERY_HIGH_LEVEL:
			data = dict(title=f"Battery reached {battery.percent}%", msg="Please plug out the charger.")
			notify(**data)
	else:
		if battery.percent <= BATTERY_LOW_LEVEL:
			data = dict(title=f"Battery is low {battery.percent}%", msg="Please plug in the charger.")
			notify(**data)

def main():
	global max_notification
	try:
		while True:
			show_notification()
			sleep(30)
	except (KeyboardInterrupt, EOFError):
		os.remove("settings.json")
		sys.exit(0)

if __name__ == "__main__":
	main()
