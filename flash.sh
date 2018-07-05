#!/bin/bash
screen -X -S coink kill
ampy --port /dev/ttyUSB0 put boot.py
ampy --port /dev/ttyUSB0 put capture.py
