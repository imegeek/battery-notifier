from tkinter import Tk
from tkinter import (
	StringVar,
	IntVar,
	Label,
	Frame,
	Canvas,
	LabelFrame,
	Button,
)

from tkinter import messagebox
import os
import json
import psutil
import subprocess
from PIL import Image, ImageTk
from tkSliderWidget import Slider
from winotify import Notification, audio

path = os.path.split(os.path.realpath(os.path.abspath(__file__)))[0]
settings_file = os.path.join(path, "settings.json")
service_path = os.path.join(path, "battery_process.pyw")

root = Tk()
root.title("Battery Notifier")
root.resizable(0, 0)

window_width = 600
window_height = 400

# Get the screen width and height.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center coordinates for positioning the window.
x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))

# Set the geometry of the window to be centered on the screen.
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
root.iconbitmap(os.path.join(path, "src\\icon.ico"))

battery_percent = StringVar()
is_plugged = StringVar()
service_status = StringVar()
service_button_text = StringVar()
service_pid = IntVar()
startup_button_value = IntVar()

try:
	settings = json.load(open(settings_file))
	high_battery_level = settings["battery_high_level"]
	low_battery_level = settings["battery_low_level"]
	pid = settings["pid"]
except Exception:
	high_battery_level = 80
	low_battery_level = 20
	pid = -1

# print(settings)
service_pid.set(pid)

def notify(title, msg=""):
	toast = Notification(
		app_id = "Battery Notifier",
		title = title,
		msg= msg,
		duration="short",
		icon=os.path.join(path, "src\\icon_96px.png")
	)
	toast.set_audio(sound=audio.Mail, loop=False)
	return toast.show()

def is_process_running(pid):
	return psutil.pid_exists(pid)

def update_data(bypass=False):
	pid = service_pid.get()
	if is_process_running(pid):
		service_status.set("Running")
		service_button_text.set("Stop Service")
		service_label.config(fg="green")
	else:
		service_status.set("Not running")
		service_button_text.set("Start Service")
		service_label.config(fg="red")

	battery = psutil.sensors_battery()
	battery_percent.set(f"{battery.percent}%")

	if battery.power_plugged == 0:
		bypass = False
		canvas.coords(battery_fill, 0, 0, (46 / 100) * battery.percent, 100)
	else:
		if not bypass:
			root.after(100, battery_config)
			bypass = True

	if battery.percent <= 30:
		canvas.itemconfig(battery_fill, fill="red")
	else:
		canvas.itemconfig(battery_fill, fill="#00b900")

	if battery.percent == 100:
		battery_nip_fill.config(bg="#00b900")
	else:
		battery_nip_fill.config(bg="#fff")


	if battery.power_plugged == 0:
		is_plugged.set("Discharging")
		charging_lable.config(fg="red")
		canvas.itemconfig(bolt, state="hidden")
	else:
		is_plugged.set("Charging")
		charging_lable.config(fg="green")
		# battery_fill.config(bg="#00b900")
		canvas.itemconfig(bolt, state="normal")
		canvas.itemconfig(battery_fill, fill="#00b900")

	root.after(500, update_data, bypass)

def battery_config(value=0, repeat=False):
	battery = psutil.sensors_battery()
	if battery.power_plugged != 0:
		canvas.itemconfig(bolt, state="normal")
		
		if not repeat:
			if value == 100:
				repeat = True
			canvas.coords(battery_fill, 0, 0, (46 / 100) * value, 100)
			battery_nip_fill.config(bg="#fff")		
		else:
			repeat = False
			battery_nip_fill.config(bg="#00b900")

		if not repeat:
			if value == 100:
				value = 0
			else:
				value += 20

		root.after(500, battery_config, value, repeat)
	else:
		canvas.itemconfig(bolt, state="hidden")

def start_service(pid, execute=True):
	if execute:
		service_pid.set(0)
		root.attributes('-disabled', 1)
		button.config(state="disabled")
		notify(title="Program started.")
		service_label.config(fg="red")
		service_button_text.set("Stop Service")
		root.after(1000, start_service, pid, False)
	else:
		try:
			max_battery = slider1.getValues()[0]
			min_battery = slider2.getValues()[0]

			process = subprocess.Popen(["pythonw", service_path])
			pid = process.pid
			with open(settings_file, "w") as f:
				data = {
					"battery_high_level": max_battery,
					"battery_low_level": min_battery,
					"pid": pid
				}
				f.write(json.dumps(data))
		except Exception:
			service_pid.set(-1)

		service_pid.set(pid)
		service_status.set("Running")
		service_label.config(fg="green")
		button.config(state="normal")
		root.attributes('-disabled', 0)

def stop_service(pid):
	os.kill(pid, 9)
	service_pid.set(-1)
	try:
		startup_button_value.set(0)
		manage_startup()
		os.remove(settings_file)
	except Exception:
		pass
	service_label.config(fg="red")
	notify(title="Program stopped.")
	service_status.set("Not running")
	service_button_text.set("Start Service")

def manage_service():
	pid = service_pid.get()

	if not is_process_running(pid):
		start_service(pid)
	else:
		stop_service(pid)

def change_startup(path, data, value):
	with open(path, "w") as f:
		data["startup"] = value
		f.write(json.dumps(data))

def manage_startup():
	if os.path.exists(settings_file):
		value = startup_button_value.get()
		data = json.load(open(settings_file))

		if os.path.exists(settings_file):
			change_startup(settings_file, data, value=0)

Label(text="Battery Notifier", font=("Verdana", 22), fg="#3d3d3d").pack(pady=5)

main_frame = Frame(width=550, height=300, relief="ridge", borderwidth=4)
main_frame.place(x=25, y=60)

slider_frame1 = LabelFrame(main_frame, text="High Battery Level: 80", width=515, height=70, borderwidth=2, relief="ridge", font=("Verdana", 10))
slider_frame1.place(x=15, y=20)

slider_frame2 = LabelFrame(main_frame, text="Low Battery Level: 20", width=515, height=70, borderwidth=2, relief="ridge", font=("Verdana", 10))
slider_frame2.place(x=15, y=110)

Label(slider_frame1, text="Set Battery Level (1-100)", font=("Verdana", 8)).place(x=2, y=11)
Label(slider_frame2, text="Set Battery Level (1-100)", font=("Verdana", 8)).place(x=2, y=11)

slider1 = Slider(slider_frame1, width = 340, height = 40, min_val = 1, max_val = 100, show_value = True, init_lis=[high_battery_level])
slider1.place(x=168, y=5)

slider2 = Slider(slider_frame2, width = 340, height = 40, min_val = 1, max_val = 100, show_value = True, init_lis=[low_battery_level])
slider2.place(x=168, y=5)

slider1.setValueChangeCallback(lambda vals : slider_frame1.config(text=f"High Battery Level: {vals[0]}"))
slider2.setValueChangeCallback(lambda vals : slider_frame2.config(text=f"Low Battery Level: {vals[0]}"))

battery_frame = LabelFrame(main_frame, text="Battery", width=250, height=70, relief="ridge", borderwidth=2, font=("Verdana", 10))
battery_frame.place(x=15, y=200)

battery_cell = Frame(battery_frame, width=50, height=25, highlightbackground="#808080", highlightthickness=1)
battery_cell.place(x=5, y=10)

bolt_image = Image.open("src/bolt.png").resize((12, 15))
r, g, b, a = bolt_image.split()

# RGB channels
r = Image.eval(r, lambda x: 250)
g = Image.eval(g, lambda x: 200)
b = Image.eval(b, lambda x: 0)

bolt_image = Image.merge('RGBA', (r, g, b, a))
image = ImageTk.PhotoImage(bolt_image)

canvas = Canvas(battery_cell, width=44, height=19)
canvas.place(x=0, y=0)

battery_fill = canvas.create_rectangle(0, 0, 46, 100, fill="#00b900", outline="")
bolt = canvas.create_image(24, 11, image=image)

battery_nip = Frame(battery_frame, width=7, height=12, highlightbackground="#808080", highlightthickness=1, padx=1, pady=1)
battery_nip.place(x=54, y=17)

battery_nip_fill = Frame(battery_nip, width=3, height=8)
battery_nip_fill.pack()

percent_lable = Label(battery_frame, textvariable=battery_percent, font=("Verdana", 10))
percent_lable.place(x=66, y=10)

status_lable = Label(battery_frame, text="Status: ", font=("Verdana", 10))
status_lable.place(x=110, y=10)

charging_lable = Label(battery_frame, textvariable=is_plugged, font=("Verdana", 10))
charging_lable.place(x=164, y=10)

service_frame = LabelFrame(main_frame, text="Service", width=250, height=70, relief="ridge", borderwidth=2, font=("Verdana", 10))
service_frame.place(x=280, y=200)

status_lable = Label(service_frame, text="Status: ", font=("Verdana", 10))
status_lable.place(x=2, y=10)

service_label = Label(service_frame, textvariable=service_status, font=("Verdana", 10))
service_label.place(x=60, y=10)

button = Button(service_frame, cursor="hand2", width=10, textvariable=service_button_text, borderwidth=2, relief="ridge", command=manage_service, bg="#77C2FF", activebackground="#77C2FF", font=("Verdana", 8), padx=5, pady=5)
button.place(x=150, y=5)

update_data()
root.mainloop()
