class Persona:
    def __init__(self, atributos: list | tuple) -> None:
        self.ci, self.nombre = atributos

    def getAtributos(self) -> list:
        return [self.ci, self.nombre]

    def getCI(self):
        return self.ci
