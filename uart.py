import serial
import time 

ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

# Enviando dados

comando = input("Selecione o comando")

if comando == '1':
    ser.write(b"0xA19231")
    time.sleep(0.1)
while 1:
    x=ser.readline()
    print(x)