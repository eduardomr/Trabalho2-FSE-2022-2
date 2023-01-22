class PID:
    def __init__(self):
        self.referencia = 0.0
        self.kp = 30.0
        self.ki = 0.2
        self.kd = 400.0
        self.T = 1.0
        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def configura_constantes(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def atualiza_referencia(self, referencia):
        self.referencia = referencia

    def controle(self, saida_medida):
        if type(saida_medida) == tuple or type(saida_medida) == None:
            return 0.0
        erro = self.referencia - saida_medida
        self.erro_total += erro

        if self.erro_total >= self.sinal_de_controle_MAX:
            self.erro_total = self.sinal_de_controle_MAX
        elif self.erro_total <= self.sinal_de_controle_MIN:
            self.erro_total = self.sinal_de_controle_MIN

        delta_error = erro - self.erro_anterior
        sinal_de_controle = self.kp*erro + (self.ki*self.T)*self.erro_total + (self.kd/self.T)*delta_error

        if sinal_de_controle >= self.sinal_de_controle_MAX:
            sinal_de_controle = self.sinal_de_controle_MAX
        elif sinal_de_controle <= self.sinal_de_controle_MIN:
            sinal_de_controle = self.sinal_de_controle_MIN

        self.erro_anterior = erro
        return sinal_de_controle

