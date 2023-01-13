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
    codigo_funcao = 0xA1
    mensagem = struct.pack(">BB", endereco_rasp, codigo_funcao)
    crc_calculado = crc.calcula_crc(mensagem)
    mensagem_crc = struct.pack(">BBH", endereco_rasp, codigo_funcao, crc_calculado)
    ser.write(mensagem_crc)
if comando == '2':
    codigo_funcao = 0xA2
    mensagem = struct.pack(">BB", endereco_rasp, codigo_funcao)
    crc_calculado = crc.calcula_crc(mensagem)
    mensagem_crc = struct.pack(">BBH", endereco_rasp, codigo_funcao, crc_calculado)
    ser.write(mensagem_crc)