import uart
import gpio
import pid
import time
import struct
import i2c
import curva
import threading

pid_control = pid.PID()
pid_control.configura_constantes(30.0, 0.2, 400.0)
pid_control.atualiza_referencia(0.0)


#DEFINIÇÃO DE COMANDOS----------------------
tempos = [0, 60, 120, 240, 260, 300, 360, 420, 480, 600]
temperaturas = [25.0, 38.0, 46.0, 54.0, 57.0, 61.0, 63.0, 54.0, 33.0, 25.0]
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
global temp_referencia_curva
#-------------------------------------------
modo="manual"
estado_forno = [0,0]
resposta=None
uart.envia_recebe(estado_forno_off)
uart.envia_recebe(estado_funcionamento_off)
uart.envia_recebe(modo_manual)

def controle_manual():
    resposta = uart.envia_recebe(solicita_tmp_interna)
    temp_interna = resposta
    print("Temperatura interna: ", temp_interna)
    resposta = uart.envia_recebe(solicita_tmp_referencia)
    temp_referencia = resposta
    print("Temperatura referencia: ", temp_referencia)
    pid_control.atualiza_referencia(temp_referencia)
    valor_pwm = pid_control.controle(temp_interna)
    gpio.controle_pwm(valor_pwm)
    print("Controle de Sinal: ", valor_pwm)
    uart.envia_comando(envia_sinal_controle, int(valor_pwm))
    print(i2c.temp_ambiente())

while True:
    comando = uart.envia_recebe(le_cmd_usuario)
    if (type(comando)!=float and comando!=None):
        if comando[1] == 0xA1:
            uart.envia_recebe(estado_forno_on)
            print("Comando ligar recebido")
            estado_forno[0] = 1

        if comando[1] == 0xA2:
            uart.envia_recebe(estado_forno_off)
            if estado_forno == [1,1]:
                gpio.controle_pwm(0.0)
                gpio.stop_pwm()
            estado_forno[0] = 0
            stop_thread = True
            print("Comando desligar recebido")

        if comando[1] == 0xA3:
            uart.envia_recebe(estado_funcionamento_on)
            estado_forno[1] = 1
            gpio.start_pwm()
            print("comando aquecimento recebido")
        if comando[1] == 0xA4:
            uart.envia_recebe(estado_funcionamento_off)
            if estado_forno == [1,1]:
                gpio.controle_pwm(0.0)
                gpio.stop_pwm()
            estado_forno[1] = 0
            stop_thread = True
            print("comando desaquecimento recebido")
        if comando[1] == 0xA5:
            if modo=="manual":
                uart.envia_recebe(modo_curva)
                modo = "curva"
                print("comando modo curva recebido")
            else:
                stop_thread = True
                uart.envia_recebe(modo_manual)
                modo = "manual"
                print("comando modo manual recebido")
    if estado_forno == [1,1] and modo == "manual":
       controle_manual()
    elif estado_forno == [1,1] and modo == "curva":

        temp_referencia_curva = 25.0
        stop_thread = False
        t = threading.Thread(target=curva.atualiza_referencia, args=(tempos, temperaturas,temp_referencia_curva, stop_thread))   
        t.start()
        curva.controle_curva(temp_referencia_curva)
    time.sleep(0.5)    
    
    
        