'''
Using tinkerforge-hardware to controll virtual joystick
'''
import joysticks,math,state

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_linear_poti import LinearPoti
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
from tinkerforge.bricklet_io4 import IO4

def io4_decode_value_bin(value):
	values={
		0: [1,1,1,1],
		1: [0,1,1,1],
		2: [0,0,1,1],
		3: [0,0,1,1],
		4: [1,1,0,1],
		5: [0,1,0,1],
		6: [1,0,0,1],
		7: [0,0,0,1],
		8: [1,1,1,0],
		9: [0,1,1,0],
		10: [1,0,1,0],
		11: [0,0,1,0],
		12: [1,1,0,0],
		13: [0,1,0,0],
		14: [1,0,0,0],
		15: [0,0,0,0]
	}
	return values[value]

HOST = "localhost"
PORT = 4223
UIDlin = "bx1"
UIDrot = "jdJ"
UIDio4 = "h4p"

ipcon = IPConnection()
poti = LinearPoti(UIDlin, ipcon)
encoder = RotaryEncoder(UIDrot, ipcon)
io = IO4(UIDio4, ipcon)

ipcon.connect(HOST, PORT)
encvalue=encoder.get_count(False)
enc= (encvalue%24)/24.0
if encvalue <0:
	enc=enc-1
pot=poti.get_position()/100.0

vjoy = joysticks.get("vJoy Device")

reverse=state.get("rev",False)
buttonRot=not encoder.is_pressed()
if(buttonRot and pot<=0.2 and not reverse):
	state.set("rev", True)
elif(reverse and pot>=-0.2 and buttonRot):
	state.set("rev", False)
reverse=state.get("rev",False)

if(reverse):
	pot*=-1
vjoy.setAxis(2, pot)
vjoy.setAxis(3, enc)

buttons=io4_decode_value_bin(io.get_value())
	
for i,x in enumerate(buttons):
	buttons[i]=bool(x) 
vjoy.setButton(0, buttons[0])
vjoy.setButton(1, buttons[1])
vjoy.setButton(2, buttons[2])
vjoy.setButton(3, buttons[3]) 
vjoy.setButton(4, buttonRot)

ipcon.disconnect()
