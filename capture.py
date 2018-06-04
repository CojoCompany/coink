import sys

from machine import I2C
from machine import Pin


sensor_address = 53


def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


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

    x_high = reply[0]
    x_low = (reply[4] >> 4)
    y_high = reply[1]
    y_low = (reply[4] & 0x0F)
    z_high = reply[2]
    z_low = (reply[5] & 0x0F)
    t_high = reply[3]
    t_low = (reply[5] >> 6)

    x = twos_complement((x_high << 4) + x_low, 12)
    y = twos_complement((y_high << 4) + y_low, 12)
    z = twos_complement((z_high << 4) + z_low, 12)
    t = twos_complement((t_high << 2) + t_low, 10)

    return reply, (x, y, z, t), ack


def main():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    devices = i2c.scan()

    if not sensor_address in devices:
        message = 'Sensor "{}" does not seem to be available!'
        sys.stderr.write(message.format(sensor_address))
        return

    read_sensor(i2c)


main()
