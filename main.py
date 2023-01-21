import uart
import gpio
import pid
import time
import struct

pid_control = pid.PID()
pid_control.configura_constantes(30.0, 0.2, 400.0)
pid_control.atualiza_referencia(0.0)


#DEFINIÇÃO DE COMANDOS----------------------
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
#-------------------------------------------
modo="manual"
estado_forno = [0,0]
resposta=None
uart.envia_recebe(estado_forno_off)
uart.envia_recebe(estado_funcionamento_off)
uart.envia_recebe(modo_manual)

while True:
    comando = uart.envia_recebe(le_cmd_usuario)
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
        print("comando desaquecimento recebido")
    if comando[1] == 0xA5:
        if modo=="manual":
            uart.envia_recebe(modo_curva)
            modo = "curva"
            print("comando modo curva recebido")
        else:
            uart.envia_recebe(modo_manual)
            modo = "manual"
            print("comando modo manual recebido")
    if estado_forno == [1,1] and modo == "manual":
        resposta = uart.envia_recebe(solicita_tmp_interna)
        temp_interna = resposta
        print("Temperatura interna: ", temp_interna)
        resposta = uart.envia_recebe(solicita_tmp_referencia)
        temp_referencia = resposta
        print("Temperatura referencia: ", temp_referencia)
        pid_control.atualiza_referencia(temp_referencia)
        valor_pwm = pid_control.controle(temp_interna)
        gpio.controle_pwm(valor_pwm)
        print(valor_pwm)
        time.sleep(0.5)
        # uart.envia_recebe(envia_sinal_controle , valor_pwm)
    
        