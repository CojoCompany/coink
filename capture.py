import sys

from machine import I2C
from machine import Pin


sensor_address = 53


def read_sensor(i2c):
    reply = bytearray(6)
    sensor = 0x6b
    trigger = 1 << 7
    register = 0x00
    request = bytearray([sensor, trigger + register])

    i2c.start()
    ack = i2c.write(request)
    i2c.readinto(reply)
    i2c.stop()

    return reply, ack


def main():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    devices = i2c.scan()

    if not sensor_address in devices:
        message = 'Sensor "{}" does not seem to be available!'
        sys.stderr.write(message.format(sensor_address))
        return

    read_sensor(i2c)


main()
