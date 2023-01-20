class PID:

    def __init__(self):
        self.kp = 30.0
        self.ki = 0.2
        self.kd = 400.0
        self.referencia = 0.0
        self.erro_anterior = 0.0
        self.integral = 0.0

    def atualizar_pid(self, erro, valor_atual):
        erro = self.referencia - valor_atual
        self.integral += erro
        derivada = erro - self.erro_anterior
        self.erro_anterior = erro
        saida = self.kp * erro + self.ki * self.integral + self.kd * derivada
        print( max(min(saida, 100), -100)

# TESTE

pid = PID()
while True:
    entrada = float(input("Digite a temperatura: "))
    pid.atualizar_pid(25.0, entrada)