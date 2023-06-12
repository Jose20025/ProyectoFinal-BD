class Mascota:
    def __init__(self, listaAtributos: list | tuple = None):

        self.codMascota, self.idcliente, self.alias, self.especie, self.raza, self.color, self.fechaNac, self.size = listaAtributos

    def getCod(self):
        return self.codMascota
