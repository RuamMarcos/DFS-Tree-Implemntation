import os
from Grafo import  Grafo

def ler_grafos(arquivo_txt, limite=20):
    grafos = []
    with open(arquivo_txt, 'r') as file:
        linhas = file.read().split('\n\n')  # Separa por blocos de adjacência
        
        for bloco in linhas[:limite]:  # Limita às primeiras 'limite' listas
            if not bloco.strip():  # Ignora blocos vazios
                continue
            
            # Processa cada bloco em uma matriz de adjacência
            matriz = []
            for linha in bloco.split('\n'):
                if linha.strip():  # Ignora linhas vazias dentro do bloco
                    linha_numeros = list(map(int, linha.strip().split()))
                    matriz.append(linha_numeros)
            
            if matriz:  # Se a matriz não estiver vazia, cria o grafo
                grafos.append(Grafo(matriz))
    
    return grafos

def exibir_opcoes_matrizes(matrizes):
    quantidade = len(matrizes)
    matriz_opcoes = [f"matriz {i+1}" for i in range(quantidade)]
    
    titulo = "matrizes carregadas"
    # Calcula o comprimento do item mais longo
    maior_comprimento = max(len(f"matriz {quantidade}"), len(titulo))
    largura_caixa = maior_comprimento + 8  # Margem fixa para bordas e espaçamento
    
    # Cabeçalho
    print(f"╔{'═' * (largura_caixa - 2)}╗")
    print(f"║{titulo:^{largura_caixa - 2}}║")
    print(f"╠{'═' * (largura_caixa - 2)}╣")
    
    # Itens
    for i in range(quantidade):
        prefixo = "╟──"
        item = f"matriz {i+1}"
        espaco_restante = largura_caixa - len(item) - 5  
        print(f"{prefixo} {item}{' ' * espaco_restante}║")
    
    # Rodapé (só se houver itens)
    if quantidade > 0:
        print(f"╚{'═' * (largura_caixa - 2)}╝")

def escolher_grafo(grafos):
    os.system('cls')
    
    exibir_opcoes_matrizes(grafos)
    print("\n")
    grafo =grafos[int(input("Escolha a matriz de adjacência do grafo desejado: ")) - 1]
    return grafo

grafos = ler_grafos("grafo.txt")
grafo = escolher_grafo(grafos)

print(grafo)