import time  # Importa o módulo time para lidar com o tempo

# Define uma função para limpar uma mensagem na linha de comando
def mensagembase(n):
    print('\b' * n + ' ' * n + '\b' * n, end='', flush=True)

# Define uma função que mostra uma mensagem de espera com pontos animados
def waiting_dots(wait, ndots=4, interval=0.5, message="Esperando", final_message=None):
    start = time.time()  # Obtém o tempo atual
    print(message, end="", flush=True)  # Imprime a mensagem inicial
    while time.time() - start < wait:  # Loop enquanto o tempo decorrido for menor que o tempo de espera
        for _ in range(ndots):  # Loop para cada ponto a ser exibido
            print('.', end='', flush=True)  # Imprime um ponto
            time.sleep(interval)  # Aguarda um intervalo de tempo
        mensagembase(ndots)  # Limpa os pontos
        time.sleep(interval)  # Aguarda um intervalo de tempo
    if final_message is not None:  # Se houver uma mensagem final especificada
        mensagembase(len(message))  # Limpa a mensagem inicial
        print(final_message)  # Imprime a mensagem final
