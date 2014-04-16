tinkerforge-joystick
====================

Using Tinkerforge hardware to emulate a virtual joystick for Windows, by using SimScript ( https://code.google.com/p/fscode/wiki/SimScript ) 

## Installation

1. install SimScript and VJoy
2. edit _joystick-server.py_ and _scripts/joystick-client.py_ to fit your needs/UIDs
3. copy _scripts/joystick-client.py_ to _scripts_ in your SimScript-dir
6. start _joystick-server.py_ using python3
5. start SimScript and select _joystick-client.py_
7. done

## My Tinkerforge-setup

###	IO4

1. button 1
2. button 2
3. button 3
4. indicator (led) for reverse of linear poti

###	Linear Poti

controls 3. axis (positive only, until reversed)

###	Rotary Encoder

* rotary: controls 4. axis
* button: reverses linear poti, also button 5 of virtual controler
