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

# ENVIO DE MENSAGENS
estado_forno_on = [0x01, 0x16, 0xD3, *matricula, 1]
estado_forno_off = [0x01, 0x16, 0xD3, *matricula, 0]
solicita_tmp_interna = [0x01, 0x23, 0xC1, *matricula]
solicita_tmp_referencia = [0x01, 0x23, 0xC2, *matricula]
le_cmd_usuario = [0x01, 0x23, 0xC3, *matricula]
envia_sinal_controle = [0x01, 0x16, 0xD1, *matricula] # + Int de valor
envia_sinal_referencia = [0x01, 0x16, 0xD2, *matricula] # + Float de valor
modo_manual = [0x01, 0x16, 0xD4, *matricula, 0]
modo_curva = [0x01, 0x16, 0xD4, *matricula, 1]
estado_funcionamento_on = [0x01, 0x23, 0xD5, *matricula, 1]
estado_funcionamento_off = [0x01, 0x23, 0xD5, *matricula, 0]

def envia_comando(comando,valor = None):
  msg = bytes(comando)
  if valor != None and type(valor) == int:
    valor = struct.pack('<i',valor)
  elif valor != None and type(valor) == float:
    valor = struct.pack('<f',valor)
  if valor != None:
    msg = msg + valor
  crc_calculado = crc.calcula_crc(msg,len(msg))
  mensagem_crc = msg+ crc_calculado.to_bytes(2, 'little')
  uart0_filestream.write(mensagem_crc)


def recebe_resposta():
  resposta = uart0_filestream.read(9)
  if len(resposta) != 9:
    print("Erro de comunicação")
    return None
    
  info = resposta[3:6]
  cod = resposta[3]

  crc_calculado = crc.calcula_crc(resposta,len(resposta)-2)
  crc_recebido = struct.unpack('<H',resposta[-2:])[0]
  if crc_calculado == crc_recebido:
    if cod == 0xC1 or cod == 0xC2:
      return round(struct.unpack('<f', info)[0],2)
    if cod == 0xD1 or cod == 0xD2:
      return resposta
    return cod, struct.unpack('<i', info)[0]
  else:
    print("Erro de CRC")
    return None

def envia_recebe(comando,valor = None):
  envia_comando(comando,valor)
  time.sleep(0.5)
  return recebe_resposta()

# TESTE

""" while True:
  entry = input("Digite o comando: ")
  if entry == "1":
    envia_recebe(estado_forno_on)
  elif entry == "2":
    envia_recebe(estado_forno_off)
  elif entry == "3":
    envia_recebe(solicita_tmp_interna)
  elif entry == "4":
    envia_recebe(solicita_tmp_referencia)
  elif entry == "5":
    envia_recebe(le_cmd_usuario)
  elif entry == "6":
    envia_recebe(envia_sinal_controle, 100)
  elif entry == "7":
    envia_recebe(envia_sinal_referencia, 40.0)
  elif entry == "8":
    envia_recebe(modo_manual)
  elif entry == "9":
    envia_recebe(modo_curva)
  elif entry == "10":
    envia_recebe(estado_funcionamento_on)
  elif entry == "11":
    envia_recebe(estado_funcionamento_off)
  else:
    print("Comando inválido")
 """