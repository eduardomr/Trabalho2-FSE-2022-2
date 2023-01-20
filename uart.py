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
matricula = [9,2,3,1]
estado_led_on = [0x01, 0x16, 0xD3, *matricula, 1]
estado_led_off = [0x01, 0x16, 0xD3, *matricula, 0] 


while True:
  comando = input("Selecione o comando")

  if comando == '1':
      msg = bytes(estado_led_on)
      crc_calculado = crc.calcula_crc(msg,len(msg))
      mensagem_crc = msg+ crc_calculado.to_bytes(2, 'little')
      uart0_filestream.write(mensagem_crc)

  if comando == '2':
    msg = bytes(estado_led_off)
    crc_calculado = crc.calcula_crc(msg,len(msg))
    mensagem_crc = msg+ crc_calculado.to_bytes(2, 'little')
    uart0_filestream.write(mensagem_crc)
