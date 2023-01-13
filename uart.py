import serial
import time
import struct
import crc

ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

# MODBUS
endereco_rasp = 0x01





comando = input("Selecione o comando")

if comando == '1':
    código_função = 0xA1
    comando_enviado = struct.pack(">BBH", endereco_rasp, código_função, crc.calcula_crc(código_função,1))
    ser.write(comando_enviado)
if comando == '2':
    código_função = 0xA2
    comando_enviado = struct.pack(">BBH", endereco_rasp, código_função, crc.calcula_crc(código_função,1))
    ser.write(comando_enviado)