import csv
import time
import struct
import pid
import gpio
import uart
import threading


pid_curva = pid.PID()
pid_curva.configura_constantes(30.0, 0.2, 400.0)
pid_curva.atualiza_referencia(0.0)
matricula = [9,2,3,1]
solicita_tmp_interna = [0x01, 0x23, 0xC1, *matricula]
envia_sinal_referencia = [0x01, 0x16, 0xD2, *matricula] # + Float de valor
gpio.start_pwm()

global temp_referencia

def change_params():
    while True:
        with open('curva_reflow.csv') as csvfile:
            csv_reader_thread = csv.reader(csvfile, delimiter=',')
            csv_reader_thread.__next__()
            for row in csv_reader_thread:
                time.sleep(float(row[0]))
                temp_referencia = float(row[1])
                print("Temperatura de Referência: ", temp_referencia)
                uart.envia_recebe(envia_sinal_referencia, temp_referencia)
                pid_curva.atualiza_referencia(temp_referencia)
                

def controle_curva():
    threading.Thread(target=change_params).start()
    while True:
        resposta = uart.envia_recebe(solicita_tmp_interna)
        temp_interna = resposta
        print("Temperatura interna: ", temp_interna)
        valor_pwm = pid_curva.controle(temp_interna)
        gpio.controle_pwm(valor_pwm)
        print("Controle de Sinal: ", valor_pwm)
        time.sleep(0.5)

    

controle_curva()
