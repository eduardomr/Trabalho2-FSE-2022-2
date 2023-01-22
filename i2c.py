import bme280
import smbus2
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def temp_ambiente():
    bme280_data = bme280.sample(bus,address)
    ambient_temperature = bme280_data.temperature
    return ambient_temperature





        