#!/bin/sh

.PHONY: default clean

default:
	sudo pigpiod
	sudo python3 app.py

clean:
	sudo rm -rf ./*/__pycache__
	sudo rm -rf ./*/*.pyc
