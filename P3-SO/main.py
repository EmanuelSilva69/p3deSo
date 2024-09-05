import sys
from argparse import *
from exceptions import *
from mensagem import *
from raids import  *
from organizacao import *
from arquivo import *


def main():
    # Tela de login
    while True:
        opcao = tela_de_login()
        if opcao == 1:
            break
        elif opcao == 2:
            informacoes()

    # Parâmetros do RAID
    nivel, numero_de_discos, tamanho_disco, frases = parametros()


    # Obtenção das frases a serem escritas
    lista = []
    for _ in range(frases):
        organizacao()
        frase = input("\033[34mDigite uma frase: \033[0m\n")
        organizacao()
        lista.append(frase)


    organizacao()
    print("Agora, vamos simular uma falha ")
    organizacao()

    # Simulação de falha
    while True:
        try:
            organizacao()
            simulacao_falha = int(input("Digite qual disco deve falhar:\n - "))
            organizacao()
            if 0 <= simulacao_falha < numero_de_discos:
                break
            else:
                organizacao()
                print('Digite um número válido de disco:')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um número válido de disco:')
            organizacao()

    # Falha de todos os discos
    while True:
        try:
            falhartudo = int(input("Quer falhar TODOS os discos? (1 pra sim, 0 para não)):\n - "))
            if falhartudo in (0, 1):
                break
            else:
                organizacao()
                print('Digite um valor válido (0, 1).')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um valor válido (0, 1).')
            organizacao()

    # Reconstrução do disco
    while True:
        try:
            reconstruir = int(input("Deseja reconstruir o disco? (1 para sim, 0 para não)\n - "))
            if reconstruir in (0, 1):
                break
            else:
                organizacao()
                print('Digite um valor válido (0 ou 1).')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um valor válido (0 ou 1).')
            organizacao()
    
    pause = reconstruir
    waiting_dots(3, message="\033[36m"+"configurando"+'\033[0m', final_message="terminado!")
    
    
    num_disks = numero_de_discos
    disk_cap = tamanho_disco
    data = lista
    falha = simulacao_falha

    if disk_cap < 0:
        print("Capacidade do disco não pode ser menor que 0 bytes.")
    if falha >= num_disks:
        print("Não pode falhar o disco: " + repr(falha) + ": Pois é um número inválido de disco")
    
    # Escolha do controlador RAID
    if nivel == 4:
        controller = ControladorRAID4(num_disks, disk_cap)
    elif nivel == 0:
        controller = ControladorRAID0(num_disks, disk_cap)
    else:
        print("Escolha um nível correto.")
    
    # Escrever os arquivos no RAID
    arquivos = []
    for i in range(len(data)):
        f = ArquivosdeRAID(i, data[i])
        arquivos.append(f)
        try:
            controller.escreve_arquivo(f)
        except DiskFullException as e:
            controller.print_data()
            sys.exit(e.msg)

    controller.print_data()  # Imprime o bloco de texto
    print(controller.ler_todos_dados())  # Imprime a frase
    orig_disks = list(controller.disks)

    if falhartudo == 1:
        fail_disks(range(num_disks), controller, orig_disks, pause)
    elif falhartudo == 2:
        for g in range(num_disks):
            controller.falhar_disco(g)
            controller.print_data()
            print(controller.ler_todos_dados())
    else:
        fail_disks([falha], controller, orig_disks, pause)

    print(controller.ler_todos_dados())

def fail_disks(disks, controller, orig_disks, pause=0):
    for x in disks:
        controller.falhar_disco(x)
        controller.print_data()
        print(controller.ler_todos_dados())
        if pause == 1:
            organizacao()
            input("Pressione enter para continuar:\n ")
            organizacao()

            controller.reconstruir_disco(x)
            controller.print_data()

        try:
            controller.validar_disco(orig_disks)
        except DiskReconstructException as e:
            print(e.msg)

if __name__ == "__main__":
    main()
