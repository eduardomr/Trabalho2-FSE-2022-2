import bme280
import RPi_I2C_driver
import smbus2
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def temp_ambiente():
    bme280_data = bme280.sample(bus,address)
    #humidity  = bme280_data.humidity
    #pressure  = bme280_data.pressure
    #ambient_temperature = bme280_data.temperature
    return bme280_data


        