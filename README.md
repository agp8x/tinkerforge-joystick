tinkerforge-joystick
====================

Using Tinkerforge hardware to emulate a virtual joystick for Windows, by using SimScript ( https://code.google.com/p/fscode/wiki/SimScript ) 

## Installation

1. install SimScript and VJoy
2. edit _scripts/tinkerforge.py_ to fit your needs/UIDs
3. copy _scripts/tinkerforge.py_ to _scripts_ in your SimScript-dir
4. copy _modules/tinkerforge_ to _modules_ in your SimScript-dir
5. start SimScript and select _tinkerforge.py_
6. check log of SimScript for errors
7. done

## Notes

The script takes too long to run, so input is sometimes delayed and log is spammed with warnings
