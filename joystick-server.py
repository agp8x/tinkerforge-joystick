#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import socketserver

DEV = False

LISTEN = ("localhost", 1337)
HOST = "localhost"
PORT = 4223
UIDlin = "bx1"
UIDrot = "jdJ"
UIDio4 = "h4p"

if not DEV:
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
	#make sure a pressed button always makes its way to the client
	for i,x in enumerate(new):
		if not values[2][i+1] and x:
			values[2][i+1] = True
			new_values[i+1] = True
		elif values[2][i+1] and not x:
			new_values[i+1] = False

def served():
	global values
	for i,x in enumerate(new_values):
		values[2][i] = 1 if x else 0
def handle_set(data):
	data=data.strip().split(':')[1]
	name, value= data.split('=')
	device, port = name.split('_')
	port=int(port)
	value=int(value)
	#validate to keep hardware safe
	if device == "io4":
		if port == 3:
			if DEV:
				print("set",device,port,"to",value)
			else:
				io.set_value(8*value)

class TfServer(socketserver.StreamRequestHandler):
	def handle(self):
		global values
		self.data = self.rfile.readline().strip().decode("utf-8")
		#if self.data == "get":
		self.request.sendall(bytes(str(values), "utf-8"))
		self.data = self.rfile.readline().decode("utf-8").strip()
		handle_set(self.data)
		served()

if __name__ == "__main__":
	if not DEV:
		ipcon = IPConnection()
		poti = LinearPoti(UIDlin, ipcon)
		encoder = RotaryEncoder(UIDrot, ipcon)
		io = IO4(UIDio4, ipcon)
		#connect
		ipcon.connect(HOST, PORT)
		#setup
		poti.set_position_callback_period(50)
		encoder.set_count_callback_period(50)
		io.set_configuration(7, 'i', True)
		io.set_configuration(8, 'o', False)
		io.set_interrupt(7)
		poti.register_callback(poti.CALLBACK_POSITION, cb_lin)
		encoder.register_callback(encoder.CALLBACK_COUNT, cb_rot)
		encoder.register_callback(encoder.CALLBACK_PRESSED, cb_rotpr)
		encoder.register_callback(encoder.CALLBACK_RELEASED, cb_rotre)
		io.register_callback(io.CALLBACK_INTERRUPT, cb_interrupt)
		#initial values
		values[0] = encoder.get_count(False)
		values[1] = poti.get_position()
		values[2] = [not encoder.is_pressed()] + io4_decode_value_bin(io.get_value())
	server = socketserver.TCPServer(LISTEN, TfServer)
	server.allow_reuse_address = True
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("Exit gracefully")
	if not DEV:
		ipcon.disconnect()
	print("done")

