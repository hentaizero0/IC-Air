#!/bin/sh

.PHONY: default clean

default:
	sudo python3 app.py

clean:
	rm -rf ./*/__pycache__
	rm -rf ./*/*.pyc
