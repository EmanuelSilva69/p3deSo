bin_format = '#010b'  # Formato binário para armazenar dados. '#010b' = 8 bits/1 byte sem incluir '0b' anexado

# Classe para manipular os arquivos da raid (ler, escrever, transformar em string etc.)
class ArquivosdeRAID:
    data_B = [] #dados dos arquivos de bloco
    start_addr = None
    padding = 0
    def __init__(self, file_id, data): #iniciando as informações do arquivo
        self.id = file_id #identificação do arquivo
        self.data_S = data #dados
        self.data_B = self.converter_em_string(data) #data convertida em string

    # Comando de leitura
    def __len__(self):
        return len(self.data_B)

    # comando para representar o arquivo e sua informação
    def __repr__(self):
        return repr(self.id) + ": '" + self.data_S + "'"

    # comando de igualdade
    def __eq__(self, other):
        if type(other) is type(self):
            return self.data_B == other.data_B
        return False
    # comando de negação
    def __ne__(self, other):
        return not self.__eq__(other)

    #Comando para converter os dados em string.

    @staticmethod
    def converter_em_string(d):
        bin_list = []
        for x in d: #-> parte transformando a palavra em número (inteiro)
            bin_list.append(
                format(ord(x), bin_format))  # Modifica o caractere para inteiro e depois  para binário e adiciona no fim da lista
        return bin_list #retorna a lista em forma de binário
    @staticmethod
    def from_bits(file_id, b): #converter de binário pra inteiro e depois para string (processo reverso do de cima ai)
        ret_str = "" #define a variável como vazia, que vai receber as palavras
        for x in b:
            ret_str += chr(int(x, 2)) #o int transforma em inteiro, e depois o chr transforma em letra, ai soma, formando a string.
        return ArquivosdeRAID(file_id, ret_str)
