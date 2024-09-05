from abc import ABCMeta, abstractmethod
import warnings
from arquivo import *
from disk import Disco
from exceptions import *
from mensagem import waiting_dots

# Controlador do processo da RAID básico (Classe abstrata)
class ControladorRAID(metaclass=ABCMeta):
    arquivos = []
    disks = []

    def __init__(self, num_disks,disk_cap=0):  # atribui um valor para a variavel do numero de disco e o máximo de disco.
        self.num_disks = num_disks
        self.disk_cap = disk_cap
        for i in range(num_disks):
            self.disks.append(Disco(i, disk_cap))

    # leitura do disco do inicio
    def __len__(self):
        return len(self.disks[0])

    # Retorna uma linha de dados do disco
    def get_linhacd(self, index):
        block = []
        for i in range(len(self.disks)):
            try:
                block.append(self.disks[i].read(index))
            except IndexError:
                print(
                    "Este erro é gerado quando o valor do índice fornecido é negativo ou excede o comprimento da sequência")
                pass
        return block

    # comando de escrever o arquivo
    def escreve_arquivo(self, arq):
        if len(self.arquivos) == 0: #arquivo vazio
            arq.start_addr = 0
        else:
            arq.start_addr = len(self) #arquivo não vazio

        self.arquivos.append(arq)
        blocks = list(split_data(arq.data_B, len(self.disks) - 1)) #separa os dados do arquivo em blocos
        arq.padding = (len(self.disks) - 1) - len(blocks[-1]) #separa os blocos um do outro, para n ficar um monte de número binário desorganizado
        self.escreve_parte(arq.data_B + [format(0, '#010b')] * arq.padding) #escreve o fragmento de texto no hd
    #Comando para validar se o conteúdo do disco é... válido
    def validar_disco(self, orig_disks=None):
        for i in range(len(self)):
            # Esse comando  Valida a paridade de um bloco removendo cada item em sequência, calculando a paridade dos itens restantes  e comparando o resultado com o item removido.
            self.validar_paridade(self.get_linhacd(i))
        if orig_disks is not None:
            for i in range(len(orig_disks)):
                if orig_disks[i] != self.disks[i]:
                    raise DiskReconstructException("Reconstrução de disco falhou: Disco " + repr(i) + " está corrompido")
    @abstractmethod
    def escreve_parte(self, data):
        pass

    @abstractmethod
    def ler_todos_dados(self):
        pass

    @abstractmethod
    def ler_todos_arquivos(self):
        pass

    @abstractmethod
    def falhar_disco(self, disk_num):
        pass

    @abstractmethod
    def reconstruir_disco(self, disk_num):
        pass

    @abstractmethod
    def validar_paridade(self, disk_num):
        pass

# RAID4
class ControladorRAID4:
    __metaclass__ = ControladorRAID #fazendo a herança dos dados da classe abstrata ControladorRAID
    disks = []
    arquivos = []

    def __init__(self, num_disks,
                 disk_cap=0):  # atribui um valor para a variavel do numero de disco e o máximo de disco.
        self.num_disks = num_disks
        self.disk_cap = disk_cap
        for i in range(num_disks):
            self.disks.append(Disco(i, disk_cap))

        # leitura do disco do inicio

    def __len__(self):
        return len(self.disks[0])
    def validar_disco(self, orig_disks=None):
        for i in range(len(self)):
            # Esse comando  Valida a paridade de um bloco removendo cada item em sequência, calculando a paridade dos itens restantes  e comparando o resultado com o item removido.
            self.validar_paridade(self.get_linhacd(i))
        if orig_disks is not None:
            for i in range(len(orig_disks)):
                if orig_disks[i] != self.disks[i]:
                    raise DiskReconstructException("Reconstrução de disco falhou: Disco " + repr(i) + " está corrompido")
    def get_linhacd(self, index):
        block = []
        for i in range(len(self.disks)):
            try:
                block.append(self.disks[i].read(index))
            except IndexError:
                print(
                    "Este erro é gerado quando o valor do índice fornecido é negativo ou excede o comprimento da sequência")
                pass
        return block
    def escreve_arquivo(self, arq):
        if len(self.arquivos) == 0: #arquivo vazio
            arq.start_addr = 0
        else:
            arq.start_addr = len(self) #arquivo não vazio

        self.arquivos.append(arq)
        blocks = list(split_data(arq.data_B, len(self.disks) - 1)) #separa os dados do arquivo em blocos
        arq.padding = (len(self.disks) - 1) - len(blocks[-1]) #separa os blocos um do outro, para n ficar um monte de número binário desorganizado
        self.escreve_parte(arq.data_B + [format(0, '#010b')] * arq.padding) #escreve o fragmento de texto no hd
    #escreve uma sequencia de bits nos discos de RAID

    def escreve_parte(self,data):
        blocks = split_data(data, len(self.disks) - 1)
        for x in blocks:
        #Calcula o bit de paridade para o bloco x. Precisamos converter as strings bin em inteiros para usar a manipulação de bits para calcular o XOR
            parity_bit = self.calcular_paridade(x)
            self.validar_paridade(x + [format(parity_bit, bin_format)])
            parity_disk = self.calcular_paridade_disco(len(self))
        #O comando abaixo insire o bit de paridade no bloco na posição do disco de paridade atual
            x.insert(parity_disk, format(parity_bit, bin_format))
        # Escreve cada bloco de texto nos discos
            for i in range(len(x)):
                self.disks[i].write(x[i])
    #comando de ler a sequencia de bits nos discos de RAID, lendo todos os dados nos discos, ignorando bits de paridade e preenchimento. Não leva em conta discos ausentes.
    def ler_todos_dados(self):
        ret_str = ''
        for i in range(len(self)):
            for j in range(len(self.disks)):
                parity_disk = self.calcular_paridade_disco(i)
                if j != parity_disk:
                    ret_str += chr(int(self.disks[j].read(i), 2))  #Converte a string binária para inteiros, e depois para caracteres
            for k in range(len(self.arquivos)):
                if i == self.arquivos[k].start_addr - 1:
                    ret_str = ret_str[:len(ret_str) - self.arquivos[k - 1].padding]

        ret_str = ret_str[:len(ret_str) - self.arquivos[-1].padding]
        return ret_str
    #comando de ler todos os arquivos guardados nos discos de RAID
    def ler_todos_arquivos(self):
        ret_bits = []
        ret_arquivos = []
        for i in range(len(self)):
            for j in range(self.num_disks):
                parity_disk = self.calcular_paridade_disco(i)
                if j != parity_disk:
                    ret_bits.append(self.disks[j].read(i))
            for k in range(len(self.arquivos)):
                if i == self.arquivos[k].start_addr - 1:
                    ret_bits = ret_bits[:len(ret_bits) - self.arquivos[k - 1].padding]
                    ret_arquivos.append(ArquivosdeRAID.from_bits(k - 1, ret_bits))
                    ret_bits = []
        ret_bits = ret_bits[:len(ret_bits) - self.arquivos[-1].padding]
        ret_arquivos.append(ArquivosdeRAID.from_bits(self.arquivos[-1].id, ret_bits))
        return ret_arquivos
    #Simula uma falha de disco, por meio de uma remoção dele da lista
    def falhar_disco(self,disk_num):
        print('\033[31m'+"Disco " + repr(disk_num) + " falhou!!"+'\033[0m')
        del self.disks[disk_num]
    #Reconstroi o disco que foi falhado no comando acima
    def reconstruir_disco(self, disk_num):
        waiting_dots(3, message=('\033[32m'+"reconstruindo"+'\033[0m'), final_message="\033[31m"+"Completamente Reconstruido!"+"\033[0m'")
        if (self.num_disks - len(self.disks)) > 1:
            raise DiskReconstructException("Não foi possível reconstruir, muitos discos estão falhos e/ou ausentes!")

        new_disk = Disco(disk_num, self.disk_cap)
        for i in range(len(self.disks[0])):
            block = []
            for j in range(len(self.disks)):
                block.append(self.disks[j].read(i))
            self.validar_paridade(block + [format(self.calcular_paridade(block), bin_format)])

            new_disk.write(format(self.calcular_paridade(block), bin_format))
        self.disks.insert(disk_num, new_disk)
        self.validar_disco()
    #função para calcular o disco para armazenar bits de paridade para o bloco atual. No RAID-4 toda a paridade é armazenada em um único disco, então armazenamos no disco n-1
    def calcular_paridade_disco(self, index):
        return self.num_disks - 1
    #função para imprimir no terminal os dados em binário.
    def print_data(self):
        for x in self.disks:
            print("|   " + repr(x.disk_id) + "    ", end="")
        print("|")
        for i in range(len(self.disks)):
            print("---------", end="")
        print("-")
        for i in range(len(self.disks[0])):
            parity_disk = self.calcular_paridade_disco(i)
            for j in range(len(self.disks)):
                if i < len(self.disks[j]):
                    if self.disks[j].disk_id == parity_disk:
                        print("|" + self.disks[j].read(i)[2:], end="")
                        print(end="")
                    else:
                        print("|" + self.disks[j].read(i)[2:], end="")
                        print( end="")
            print("|", end="")
            for f in self.arquivos:
                if i == f.start_addr:
                    print("'\033[34m'<- Arquivo número:  " + repr(f.id + 1)+'\033[0m', end="") #botei um mais 1 ai pra ficar melhor pra visualizar (Arquivo 0 é feio)
            print()
        print()
    #função para calcular o bit de paridade para o bloco. Precisamos converter as strings bin em inteiros para usar a manipulação de bits para calcular o XOR (já falei isso lá em cima ent n muda muita coisa.)
    @staticmethod
    def calcular_paridade(block):
        paridade_calculada = None
        for x in block:
            paridade_calculada = paridade_calculada ^ int(x, 2) if paridade_calculada is not None else int(x, 2)
        return paridade_calculada
    #Esse comando  Valida a paridade de um bloco removendo cada item em sequência, calculando a paridade dos itens restantes  e comparando o resultado com o item removido. (falei lá em cima tbm)
    @staticmethod
    def validar_paridade(block):
        for i in range(len(block)):
            parity = block.pop(i)
            calculated_parity = ControladorRAID4.calcular_paridade(block)
            if calculated_parity != int(parity, 2):
                raise ParityCalculationException(block, calculated_parity, int(parity, 2))
            block.insert(i, parity)

# RAID0
class ControladorRAID0:
    __metaclass__ = ControladorRAID #fazendo a herança dos dados da classe abstrata ControladorRAID
    disks = []
    arquivos = []

    def __init__(self, num_disks,
                 disk_cap=0):  # atribui um valor para a variavel do numero de disco e o máximo de disco.
        self.num_disks = num_disks
        self.disk_cap = disk_cap
        for i in range(num_disks):
            self.disks.append(Disco(i, disk_cap))

        # leitura do disco do inicio

    def __len__(self):
        return len(self.disks[0])
    def validar_disco(self, orig_disks=None):
        for i in range(len(self)):
            # Esse comando  Valida a paridade de um bloco removendo cada item em sequência, calculando a paridade dos itens restantes  e comparando o resultado com o item removido.
            self.validar_paridade(self.get_linhacd(i))
        if orig_disks is not None:
            for i in range(len(orig_disks)):
                if orig_disks[i] != self.disks[i]:
                    raise DiskReconstructException("Reconstrução de disco falhou: Disco " + repr(i) + " está corrompido")
    def get_linhacd(self, index):
        block = []
        for i in range(len(self.disks)):
            try:
                block.append(self.disks[i].read(index))
            except IndexError:
                print(
                    "Este erro é gerado quando o valor do índice fornecido é negativo ou excede o comprimento da sequência")
                pass
        return block

    @staticmethod
    def validar_paridade(block):
        waiting_dots(2, message=('\033[36m'+"é o fim"+'\033[0m\n'), final_message="\033[33m"+"Não há mais nada que se possa fazer"+"\033[0m\n")
        quit()
#!!!! repeti a parte acima pq n sei como fazer a herança de forma correta no python!!!
    #escreve uma sequencia de bits nos discos de RAID

    def escreve_parte(self,data):
        blocks = split_data(data, len(self.disks))
        for x in blocks:
    #o negócio aqui de paridade não é usado, então foi excluido!
        #Escreve cada bloco de texto nos discos
            for i in range(len(x)):
                self.disks[i].write(x[i])
    #Isso lê todos os dados nos discos, ignorando bits de paridade e preenchimento. Não leva em conta discos ausentes. (vai dar erro sse tiver algo ausente e é isso.)
    def ler_todos_dados(self):
        ret_str = ''
        for i in range(len(self)):
            for j in range(len(self.disks)):
                ret_str += chr(int(self.disks[j].read(i), 2))  #Converte a string binária para inteiros, e depois para caracteres
            for k in range(len(self.arquivos)):
                if i == self.arquivos[k].start_addr - 1:
                    ret_str = ret_str[:len(ret_str) - self.arquivos[k - 1].padding]

        ret_str = ret_str[:len(ret_str) - self.arquivos[-1].padding]
        return ret_str
    # Isso lê todos os arquivos nos discos, ignorando bits de paridade e preenchimento. Não leva em conta discos ausentes. -> (vai dar erro)
    def ler_todos_arquivos(self):
        ret_bits = []
        ret_arquivos = []
        for i in range(len(self)):
            for j in range(self.num_disks):
                try:
                    ret_bits.append(self.disks[j].read(i))
                except IndexError:
                    pass
            for k in range(len(self.arquivos)):
                if i == self.arquivos[k].start_addr - 1:
                    ret_bits = ret_bits[:len(ret_bits) - self.arquivos[k - 1].padding]
                    ret_arquivos.append(ArquivosdeRAID.from_bits(k - 1, ret_bits))
                    ret_bits = []

        ret_bits = ret_bits[:len(ret_bits) - self.arquivos[-1].padding]
        ret_arquivos.append(ArquivosdeRAID.from_bits(self.arquivos[-1].id, ret_bits))
        return ret_arquivos

    # Simula uma falha de disco, por meio de uma remoção dele da lista
    def falhar_disco(self,disk_num):
        print('\033[31m'+"Disco " + repr(disk_num) + " falhou!!"+'\033[0m\n')
        del self.disks[disk_num]
        waiting_dots(3, message=('\033[32m'+"Esse disco tá perdido"+'\033[0m'), final_message="\033[31m"+"BEM PERDIDO!"+"\033[0m\n")


    #Reconstroi o disco que foi falhado no comando acima (Fake News!!)
    def reconstruir_disco(self, disk_num):
        warnings.warn("Raid0 Não suporta reconstrução de disco!!!")
    #função para imprimir no terminal os dados em binário.
    def print_data(self):
        for x in self.disks:
            print("|   " + repr(x.disk_id) + "    ", end="")
        print("|")
        for i in range(len(self.disks)):
            print("---------", end="")
        print("-")
        for i in range(len(self.disks[0])):
            for j in range(len(self.disks)):
                if i < len(self.disks[j]):
                    print("|" + self.disks[j].read(i)[2:], end="")
            print(end="")
            for f in self.arquivos:
                if i == f.start_addr:
                    print("'\033[34m'<- Arquivo número:  " + repr(f.id+1)+'\033[0m', end="") #botei um mais 1 ai pra ficar melhor pra visualizar (Arquivo 0 é feio)
            print()
        print()
    #Função da escrita diferente porque não tem paridade
    def escreve_arquivo(self, arq):
        if len(self.arquivos) == 0: #arquivo vazio
            arq.start_addr = 0
        else:
            arq.start_addr = len(self) #arquivo não vazio

        self.arquivos.append(arq)
        blocks = list(split_data(arq.data_B, len(self.disks))) #separa os dados do arquivo em blocos
        arq.padding = len(self.disks) - len(blocks[-1]) #separa os blocos um do outro, para n ficar um monte de número binário desorganizado
        self.escreve_parte(arq.data_B + [format(0, '#010b')] * arq.padding) #escreve o fragmento de texto no hd

# Separador de Dados em partes Menores
def split_data(data, size):  
    for i in range(0, len(data), size):
        yield data[i:i + size]
