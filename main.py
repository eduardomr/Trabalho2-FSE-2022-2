import uart
import gpio
import pid
import time

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


while True:
    cod, info = uart.recebe_resposta()
    if cod == 0xA1:
        print("Comando de ligar recebido")
        uart.envia_recebe(estado_forno_on)
        estado_forno[0]=1
    if cod == 0xA2:
        print("Comando de desligar recebido")
        uart.envia_recebe(estado_forno_off)
        estado_forno[0]=0
    time.sleep(0.5)
"""  if cod == 0xA3:
        print("Comando de Iniciar Aquecimento Recebido")
        uart.envia_recebe(estado_forno_on)
        estado_forno[1]=1
    if cod == 0xA4:
        print("Comando de Parar Aquecimento Recebido")
        uart.envia_recebe(estado_forno_off)
        estado_forno[1]=0
    if cod == 0xA5:
        print("Comando Curva Recebido")
        if modo == "manual":
            modo = "curva"
            uart.envia_recebe(modo_curva)
        else:
            modo = "manual"
            uart.envia_recebe(modo_manual)
    
    if estado_forno[0]==1 and estado_forno[1]==1:
        gpio.start_pwm()
        if modo == "manual":
            #Ler temp ambiente tbm
            cod, temp_ref = uart.envia_recebe(solicita_tmp_referencia)
            pid.atualiza_referencia(temp_ref)
            cod, temp_int = uart.envia_recebe(solicita_tmp_interna)
            gpio.controle_pwm(pid_control.controle(temp_int))  """  
    