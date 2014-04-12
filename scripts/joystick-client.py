#!/usr/bin/env python2
# -*- coding: utf-8 -*- 
'''
Using tinkerforge-hardware via proxy to controll virtual joystick
'''
import joysticks,math,state
import socket

TARGET = ("localhost", 1337)
REQUEST = "get"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sock.connect(TARGET)
	sock.sendall(bytes(REQUEST))
	answer = str(sock.recv(1024))
finally:
	sock.close()
# [rotary encode, linear poti, [rotary button, io4...]]
values = eval(answer)

encvalue=values[0]
enc= (encvalue%24)/24.0
if encvalue <0:
	enc=enc-1

pot=values[1]/100.0

vjoy = joysticks.get("vJoy Device")

reverse=state.get("rev",False)

buttonRot= values[2][0]
if(buttonRot and pot<=0.2 and not reverse):
	state.set("rev", True)
elif(reverse and pot>=-0.2 and buttonRot):
	state.set("rev", False)
reverse=state.get("rev",False)

if(reverse):
	pot*=-1
vjoy.setAxis(2, pot)
vjoy.setAxis(3, enc)

buttons=values[2][1:]
	
for i,x in enumerate(buttons):
	buttons[i]=bool(x) 
vjoy.setButton(0, buttons[0])
vjoy.setButton(1, buttons[1])
vjoy.setButton(2, buttons[2])
vjoy.setButton(3, buttons[3]) 
vjoy.setButton(4, buttonRot)

