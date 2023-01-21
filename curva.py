import csv
import time
import struct
import pid
import gpio
import uart


pid_curva = pid.PID()
pid_curva.configura_constantes(30.0, 0.2, 400.0)
pid_curva.atualiza_referencia(0.0)
matricula = [9,2,3,1]
solicita_tmp_interna = [0x01, 0x23, 0xC1, *matricula]
envia_sinal_referencia = [0x01, 0x16, 0xD2, *matricula] # + Float de valor
gpio.start_pwm()

def controle_curva():
    with open('curva_reflow.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_reader.__next__()

        for row in csv_reader:
            temp_referencia = float(row[1])
            uart.envia_recebe(envia_sinal_referencia, temp_referencia)
            resposta = uart.envia_recebe(solicita_tmp_interna)
            temp_interna = resposta
            print("Temperatura interna: ", temp_interna)
            print("Temperatura referencia: ", temp_referencia)
            pid_curva.atualiza_referencia(temp_referencia)
            valor_pwm = pid_curva.controle(temp_interna)
            gpio.controle_pwm(valor_pwm)
            print("Controle de Sinal: ", valor_pwm)
            time.sleep(float(row[0]))

    gpio.controle_pwm(0.0)
    gpio.stop_pwm()

controle_curva()