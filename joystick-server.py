#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import socketserver

LISTEN = ("localhost", 1337)
HOST = "localhost"
PORT = 4223
UIDlin = "bx1"
UIDrot = "jdJ"
UIDio4 = "h4p"

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_linear_poti import LinearPoti
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
from tinkerforge.bricklet_io4 import IO4

def io4_decode_value_bin(value):
	values={
		0 : [1,1,1,1],
		1 : [0,1,1,1],
		2 : [1,0,1,1],
		3 : [0,0,1,1],
		4 : [1,1,0,1],
		5 : [0,1,0,1],
		6 : [1,0,0,1],
		7 : [0,0,0,1],
		8 : [1,1,1,0],
		9 : [0,1,1,0],
		10: [1,0,1,0],
		11: [0,0,1,0],
		12: [1,1,0,0],
		13: [0,1,0,0],
		14: [1,0,0,0],
		15: [0,0,0,0]
	}
	return values[value]

# [rotary encode, linear poti, [rotary button, io4...]]
values = [0.0, 0.0, [0,0,0,0,0]]
new_values = [0,0,0,0,0]

# Callback function for position callback (parameter has range 0-100)
def cb_lin(position):
	global values
	values[1]=position
# Callback function for count callback
def cb_rot(count):
	global values
	values[0]=count

def cb_rotpr():
	global new_values
	if not values[2][0]:
		new_values[0] = True
		values[2][0] = True

def cb_rotre():
	global new_values
	if values[2][0]:
		new_values[0]=False

# Callback function for interrupts
def cb_interrupt(interrupt_mask, value_mask):
	global new_values
	new = io4_decode_value_bin(value_mask)
	for i,x in enumerate(new):
		if not values[2][i+1] and x:
			values[2][i+1] = True
			new_values[i+1] = True
		elif values[2][i+1] and not x:
			new_values[i+1] = False

def served():
	global values
	for i,x in enumerate(new_values):
		if x:
			values[2][i] = 1
		else:
			values[2][i] = 0

class TfServer(socketserver.BaseRequestHandler):
	def handle(self):
		global values
		self.data = self.request.recv(1024).strip()
		#if self.data == "get":
		self.request.sendall(bytes(str(values), "utf-8"))
		served()

if __name__ == "__main__":
	ipcon = IPConnection()
	poti = LinearPoti(UIDlin, ipcon)
	encoder = RotaryEncoder(UIDrot, ipcon)
	io = IO4(UIDio4, ipcon)

	ipcon.connect(HOST, PORT)

	poti.set_position_callback_period(50)
	encoder.set_count_callback_period(50)

	io.set_configuration(15, 'i', True)
	io.set_interrupt(15)
	
	values[0] = encoder.get_count(False)
	values[1] = poti.get_position()
	values[2] = [not encoder.is_pressed()] + io4_decode_value_bin(io.get_value())
	

	poti.register_callback(poti.CALLBACK_POSITION, cb_lin)
	encoder.register_callback(encoder.CALLBACK_COUNT, cb_rot)
	encoder.register_callback(encoder.CALLBACK_PRESSED, cb_rotpr)
	encoder.register_callback(encoder.CALLBACK_RELEASED, cb_rotre)
	io.register_callback(io.CALLBACK_INTERRUPT, cb_interrupt)

	server = socketserver.TCPServer(LISTEN, TfServer)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("Exit gracefully")
	#input('Press key to exit\n') # Use input() in Python 3
	ipcon.disconnect()
	print("done")
