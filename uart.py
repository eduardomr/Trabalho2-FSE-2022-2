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



comando=0
comando = input("Selecione o comando")

if comando == '1':
    codigo_funcao = 0x16
    subcodigo = 0xD3
    mensagem = struct.pack(">BB4BB", endereco_rasp, codigo_funcao, subcodigo, 9, 2, 3, 1, 1 )
    crc_calculado = crc.calcula_crc(mensagem,len(mensagem))
    mensagem_crc = struct.pack(">BB4BBH", endereco_rasp, codigo_funcao,subcodigo, 9,2,3,1,1,crc_calculado)
    ser.write(mensagem_crc)
if comando == '2':
    codigo_funcao = 0x16
    subcodigo = 0xD3
    mensagem = struct.pack(">BB4BB", endereco_rasp, codigo_funcao, subcodigo, 9, 2, 3, 1, 0 )
    crc_calculado = crc.calcula_crc(mensagem,len(mensagem))
    mensagem_crc = struct.pack(">BB4BBH", endereco_rasp, codigo_funcao,subcodigo, 9,2,3,1,0, crc_calculado)
    ser.write(mensagem_crc)