import csv
import time
import pid
import gpio
import uart
import threading
import i2c


pid_curva = pid.PID()
pid_curva.configura_constantes(30.0, 0.2, 400.0)
pid_curva.atualiza_referencia(0.0)
matricula = [9,2,3,1]
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
gpio.start_pwm()

global temp_referencia
def atualiza_referencia(tempos, temperaturas):
    global temp_referencia
    x=0
    for tempo in tempos:
        time.sleep(tempo)
        temp_referencia = temperaturas[x]
        print("Referencia atualizada para: ", temperaturas[x])
        x = x+1
            
def controle_curva():
    global temp_referencia
    uart.envia_recebe(envia_sinal_referencia, temp_referencia)
    resposta = uart.envia_recebe(solicita_tmp_interna)
    temp_interna = resposta
    print("Temperatura interna: ", temp_interna)
    resposta = uart.envia_recebe(solicita_tmp_referencia)
    temp_referencia = resposta
    print("Temperatura referencia: ", temp_referencia)
    pid_curva.atualiza_referencia(temp_referencia)
    valor_pwm = pid_curva.controle(temp_interna)
    gpio.controle_pwm(valor_pwm)
    print("Controle de Sinal: ", valor_pwm)
    uart.envia_comando(envia_sinal_controle, int(valor_pwm))
    print(i2c.temp_ambiente())
            

""" Tempo (s), Temperatura
0,   25
60,  38
120,  46
240, 54
260, 57
300, 61
360, 63
420, 54
480, 33
600, 25 """


tempos = [0, 60, 120, 240, 260, 300, 360, 420, 480, 600]
temperaturas = [25, 38, 46, 54, 57, 61, 63, 54, 33, 25]

t = threading.Thread(target=atualiza_referencia, args=(tempos, temperaturas))

t.start()
while True:
    controle_curva()
    time.sleep(1)
