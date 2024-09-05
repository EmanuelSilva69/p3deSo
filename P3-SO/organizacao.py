def tela_de_login():
    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Simulador dos RAIDS 0 e 4")
    organizacao()
    print("1. Iniciar")
    print("2. Informações")
    organizacao()

    while True:
        try:
            opcao = int(input("Opção: "))
            if opcao in (1, 2):
                return opcao
            else:
                organizacao()
                print('Digite uma opção válida (1 ou 2).\n')
                organizacao()
        except ValueError:
            print('Digite uma opção válida (1 ou 2).\n')
            organizacao()

def informacoes():
    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Informações sobre o simulador dos RAIDS 0 e 4")
    organizacao()
    print("RAID 0: É um método de armazenamento que divide os dados em blocos e os distribui entre todos os discos do array.")
    print("RAID 4: É um método de armazenamento que usa um disco dedicado para paridade e distribui os dados entre os discos restantes.")
    organizacao()
    print("1. Voltar")
    organizacao()

    while True:
        try:
            opcao = int(input("Opção: "))
            if opcao == 1:
                return
            else:
                organizacao()
                print('Digite uma opção válida (1).\n')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite uma opção válida (1).\n')
            organizacao()

def parametros():
    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Escolha o Raid que deseja simular:")
    organizacao()
    print("1. Raid 0")
    print("2. Raid 4")
    print("3. Voltar")
    organizacao()

    while True:
        try:
            nivel = int(input("Opção: "))
            if nivel in (1, 2):
                nivel = 0 if nivel == 1 else 4
                break
            elif nivel == 3:
                tela_de_login()
            else:
                organizacao()
                print('Digite um valor válido (1, 2 ou 3).')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um valor válido (1, 2 ou 3).')
            organizacao()

    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Digite o número de discos.")
    organizacao()

    while True:
        try:
            numero_de_discos = int(input("- "))
            if numero_de_discos > 0:
                break
            else:
                organizacao()
                print('Digite um número válido de discos.')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um número válido de discos.')
            organizacao()

    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Digite o limite de discos.")
    print("Para tamanho ilimitado, digite 0.")
    organizacao()

    while True:
        try:
            tamanho_disco = int(input("- "))
            if tamanho_disco >= 0:
                break
            else:
                organizacao()
                print('Digite um tamanho válido para o disco.')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um tamanho válido para o disco.')
            organizacao()

    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Digite a quantidade de frases a serem digitadas.")
    organizacao()

    while True:
        try:
            frases = int(input("- "))
            if frases > 0:
                break
            else:
                organizacao()
                print('Digite um número válido de frases.')
                organizacao()
        except ValueError:
            organizacao()
            print('Digite um número válido de frases.')
            organizacao()
    
    return nivel, numero_de_discos, tamanho_disco, frases

def organizacao():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")