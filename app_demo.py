import numpy as np
import cv2
import PySimpleGUI as sg
import datetime
import time
from random import randint
from gpiozero import LED, Button

from myOmron import Omron
from myLED import Led


def img2bytes(image):
	return cv2.imencode(".png", image)[1].tobytes()

def color_circle(color):
	image = np.full((100,100,4), (0,0,0,0), np.uint8)
	cv2.circle(image, (50,50), 48, color, -1)
	cv2.circle(image, (50,50), 48, (0,0,0,255), 2)
	return img2bytes(image)

class Gui():
	def __init__(self):
		img_camera = img2bytes(np.full((480,640,3), (100, 160, 240), np.uint8))
		img_graph = img2bytes(np.full((400,400,3), (100, 160, 240), np.uint8))
		self.img_green = color_circle((0, 255, 0, 255))
		self.img_red = color_circle((0, 0, 255, 255))
		font = ('Arial',20)
		column1 = [[sg.Text("Camera", font=font)],
				   [sg.Image(img_camera, size=(640, 480), key="-CAMERA-"),
				    sg.Slider(range=(0,100), default_value=50, resolution=5, disable_number_display=True, orientation='v', size=(25, 12), key="-V_SLIDER-")],
				   [sg.Slider(range=(0,100), default_value=50, resolution=5, disable_number_display=True, orientation='h', size=(71, 12), key="-H_SLIDER-")],
				   [sg.InputText(key="-INPUTTEXT-")],
				  ]
		column2 = [[sg.Text("Btn", font=font)],
				   [sg.Image(self.img_green, key="-CAUTION-"),
				    sg.Button("LED", size=(10,5), key="-LED-")],
				   [sg.Slider(range=(0,100), default_value=100, resolution=5, orientation='h', key="-SLIDER-")],
				   [sg.Text("Graph", font=font)],
				   [sg.Image(img_graph, size=(300,200), key="-GRAPH-")],
				  ]
		layout = [[sg.Column(column1, vertical_alignment="top"),
				   sg.Column(column2, vertical_alignment="top")]
				  ]
		self.window = sg.Window("GUI sample", layout)

def main():
	omron = Omron()
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	gui = Gui()
	window = gui.window
	button = Button(21)
	
	led = Led()
	is_led = False
	rotation_time = 2		# sec
	start_time = time.time()
	
	while True:
		event, values = window.read(timeout = 20)
		if event == sg.WIN_CLOSED:
			break
		elif event == "-LED-":
			is_led = not is_led
				
		ret, frame = cap.read()
		if ret:
			if button.value:
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

			# draw time
			dt = datetime.datetime.now()
			str_dt = dt.strftime("%Y/%m/%d %H:%M:%S.%f")
			cv2.putText(frame, str_dt, (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1)
			
			# draw text
			text = values["-INPUTTEXT-"]
			v = 100-int(values["-V_SLIDER-"])
			h = int(values["-H_SLIDER-"])
			if text != "":
				x = int(640 * h / 100)
				y = int(480 * v / 100)
				color = (randint(0,255), randint(0,255), randint(0,255))
				cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)

			ret, temp, humi = omron.read()
			if ret =="OK":                              # センサー値正しく取得できていたら
				temp = round(temp, 1)                   # 温度 小数第一位まで
				humi = round(humi, 1)                   # 湿度 小数第一位まで
				print(temp, humi)

			img_camera = img2bytes(frame)
			window["-CAMERA-"].update(data=img_camera)

		if button.value:
			window["-CAUTION-"].update(data=gui.img_red)
		else:
			window["-CAUTION-"].update(data=gui.img_green)

		# LEDseigyo
		if is_led:
			elapsed_time = time.time() - start_time
			phase_shift = (elapsed_time / rotation_time) * led.LED_COUNT % led.LED_COUNT
			led.rainbow(dir=-1, phase_shift=phase_shift)
		else:
			led.turn_off()
	
			
	window.close()
	led.turn_off()


if __name__ == "__main__":
	main()
