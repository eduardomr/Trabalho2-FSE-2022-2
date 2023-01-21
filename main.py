import uart

while True:
    cod, info = uart.recebe_resposta()
    if cod == 0xA1:
        print("Comando de ligar recebido")
    