class Cliente:
    def __init__(self, listaAtributos: tuple):
        self.idcliente, self.apellido, self.nrocuenta, self.direccion, self.telefono = listaAtributos

        self.atributos = listaAtributos

    def getAtributos(self):
        return self.atributos

    def getId(self):
        return self.idcliente
