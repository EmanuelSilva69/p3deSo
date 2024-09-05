from exceptions import *

# Representa e manipula os discos em um sistema de RAID
class Disco:
    def __init__(self, disk_id, capacity=0):  # inicia a base do disco (ID, capacidade maxima e o conteudo a botar no disco, no caso a "data"
        self.disk_id = disk_id
        self.capacity = capacity
        self.data = []

    # Comando para representar o disco e sua informação, basicamente informar o conteúdo do disco
    def __repr__(self):
        return repr(self.disk_id) + ":" + repr(self.data)

    # Comando de leitura
    def __len__(self):
        return len(self.data)

    # Comando de igualdade
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    # Comando de negação
    def __ne__(self, other):
        return not self.__eq__(other)

    # Comando de Escrita
    def write(self, data):
        if (self.capacity > 0) and (len(self.data) + len(data) > self.capacity):
            raise DiskFullException(self.disk_id)  # exceção do disco cheio
        self.data.append(data)

    # Comando de leitura
    def read(self, index):
        if index >= len(self.data):
            raise DiskReadException( #Exceção de leitura no disco
                "Impossível de ler o indicador : '" + repr(index) + "'  no disco :'" + repr(self.disk_id) +
                "': Isso se dá, pois o indicador está fora dos limites pré-estabelecidos")
        return self.data[index]
