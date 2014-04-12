tinkerforge-joystick
====================

Using Tinkerforge hardware to emulate a virtual joystick for Windows, by using SimScript ( https://code.google.com/p/fscode/wiki/SimScript ) 

## Installation

1. install SimScript and VJoy
2. edit _joystick-server.py_ and _scripts/joystick-client.py_ to fit your needs/UIDs
3. copy _scripts/joystick-client.py_ to _scripts_ in your SimScript-dir
4. copy _modules/tinkerforge_ to _modules_ in your SimScript-dir
5. start SimScript and select _joystick-client.py_
6. start _joystick-server.py_ using python3
7. done

