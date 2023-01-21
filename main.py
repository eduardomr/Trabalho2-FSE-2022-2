import uart

while True:
    comando = uart.recebe_resposta()
    if comando != None:
        print(comando)
    