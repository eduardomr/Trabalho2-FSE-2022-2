import serial
import time
import struct
import crc

uart0_filestream = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

if uart0_filestream == -1:
    print('"Erro - Não foi possível iniciar a UART.\n"')
else:
    print("UART inicializada!\n")

# MODBUS
endereco_rasp = 0x01
comando=0
comando = input("Selecione o comando")


if comando == '1':
    msg =  b'0x01' + b'0x16' + b'0xD3' + bytes([9, 2, 3, 1])+ b'1'
    crc_calculado = crc.calcula_crc(msg,len(msg))
    mensagem_crc = msg+ crc_calculado.to_bytes(2, 'little')
    uart0_filestream.write(mensagem_crc)

if comando == '2':
  msg =  b'0x01' + b'0x16' + b'0xD3' + bytes([9, 2, 3, 1])+ b'0'
  crc_calculado = crc.calcula_crc(msg,len(msg))
  mensagem_crc = msg+ crc_calculado.to_bytes(2, 'little')
  uart0_filestream.write(mensagem_crc)
