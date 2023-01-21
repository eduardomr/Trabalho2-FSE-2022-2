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
resposta=None

while True:
    comando = uart.envia_recebe(le_cmd_usuario)
    if comando[1] == 0xA1:
        print(comando)
        uart.envia_recebe(estado_forno_on)
        print("RECEBEU!")
    
    time.sleep(0.5)