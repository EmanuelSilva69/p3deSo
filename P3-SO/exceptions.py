# Exceptions

# Paridade
class ParityCalculationException(Exception):  # Verifica se ocorre um erro de paridade, no caso. Se um número ímpar de bits (incluindo o bit de paridade) for transmitido incorretamente,
    # o bit de paridade estará incorreto, indicando assim que ocorreu um erro de paridade na transmissão.
    def __init__(self, block=None, experado=None, actual=None):
        self.block = block
        self.experado = experado
        self.actual = actual

        if block is None or experado is None or actual is None:  # receber um valor vazio
            msg = "Calculo de Paridade Incorreto!!"
        else:
            msg = "Calculo incorreto no \nbloco: "  # aqui fala qual bloco está com alguma disparidade
            for x in block:
                msg += x + " "
            msg += "\nEsperado:  " + repr(experado) + " (" + format(experado, '#010b') + ")\n"
            msg += "Atual:   " + repr(actual) + " (" + format(actual, '#010b') + ")\n"
        super(ParityCalculationException, self).__init__(msg)

# Exceção geral, base para as outras de disco
class DiskException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super(DiskException, self).__init__(msg)


# Essa exceção ocorrerá quando o disco estiver cheio
class DiskFullException(DiskException):
    def __init__(self, disk_id):
        self.disk_id = disk_id
        super(DiskFullException, self).__init__("Erro! O disco selecionado '" + repr(disk_id) + "' está cheio")


# Erro na leitura de disco
class DiskReadException(DiskException):
    def __init__(self, msg):
        self.msg = msg
        super(DiskReadException, self).__init__(msg)


# Erro na reconstrução do disco
class DiskReconstructException(DiskException):
    def __init__(self, msg):
        self.msg = msg
        super(DiskReconstructException, self).__init__(msg)


# Erro nos dados transmitidos. No caso, os dados foram diferentes do esperado.
class DataMismatchException(DiskException):
    def __init__(self, msg):
        self.msg = msg
        super(DataMismatchException, self).__init__(msg)

