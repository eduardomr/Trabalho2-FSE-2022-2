import RPI.GPIO as GPIO

ventoinha_pin = 24
resistor_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ventoinha_pin, GPIO.OUT)
GPIO.setup(resistor_pin, GPIO.OUT)


