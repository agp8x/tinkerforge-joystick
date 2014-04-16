#!/usr/bin/env python2
# -*- coding: utf-8 -*- 
'''
Using tinkerforge-hardware via proxy to controll virtual joystick
'''
import socket

DEV = False

if not DEV:
	import joysticks,math,state

TARGET = ("localhost", 1337)
REQUEST = "get\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sock.connect(TARGET)
	sock.sendall(bytes(REQUEST))
	answer = str(sock.recv(1024))
	# [rotary encode, linear poti, [rotary button, io4...]]
	values = eval(answer)
	if DEV:
		print("recv", answer)
		print("values",values)
	encvalue=values[0]
	enc= (encvalue%24)/24.0
	if encvalue <0:
		enc=enc-1

	pot=values[1]/100.0
	
	if DEV:
		reverse=False
	else:
		vjoy = joysticks.get("vJoy Device")
		reverse=state.get("rev",False)

	buttonRot= values[2][0]

	if(buttonRot and pot<=0.2 and not reverse):
		reverse = True
	elif(buttonRot and pot>=-0.2 and reverse):
		reverse = False
	sendstr="set:io4_3="+str(int(reverse))+"\n"
	
	if(reverse):
		pot*=-1
	buttons=values[2][1:]
	for i,x in enumerate(buttons):
		buttons[i]=bool(x) 
		if not DEV:
			vjoy.setButton(i, buttons[i])
	if DEV:
		print("reverse",reverse)
		print("pot:",pot)
		print("enc:",enc)
		print("io4:",buttons)
		print("butrot:",buttonRot)
		print("sending",sendstr)
	else:
		reverse=state.set("rev",reverse)
		vjoy.setAxis(2, pot)
		vjoy.setAxis(3, enc)
		vjoy.setButton(4, buttonRot)
	
	sock.sendall(sendstr)

finally:
	sock.close()

