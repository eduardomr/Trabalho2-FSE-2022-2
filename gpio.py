import RPi.GPIO as GPIO

ventoinha_pin = 24
resistor_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ventoinha_pin, GPIO.OUT)
GPIO.setup(resistor_pin, GPIO.OUT)

resistor_pwm = GPIO.PWM(resistor_pin, 100)
ventoinha_pwm = GPIO.PWM(ventoinha_pin, 100)

def start_pwm():
    resistor_pwm.start(0)
    ventoinha_pwm.start(0)

def stop_pwm():
    resistor_pwm.stop()
    ventoinha_pwm.stop()

def set_pwm(ventoinha, resistor):
    if ventoinha < 35:
        ventoinha = 35
    resistor_pwm.ChangeDutyCycle(resistor)
    ventoinha_pwm.ChangeDutyCycle(ventoinha)

def controle_pwm(referencia):
    if referencia > 0:
        set_pwm(0, referencia)
    else:
        set_pwm(-referencia, 0)