import matplotlib.pyplot as plt
import networkx as nx
from Grafo import Grafo
from ArvoreBusca import *
import os
import time


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

def salvar_grafo_estatico(grafo):
    nos = grafo.vertices
    arestas = grafo.arestas
    # Cria o grafo
    grafo = nx.Graph()
    
    # Adiciona nós e arestas
    grafo.add_nodes_from(str(no) for no in nos)
    grafo.add_edges_from((str(a), str(b)) for a, b in arestas)
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(grafo)  
    
    # Desenha o grafo
    nx.draw(grafo, pos, with_labels=True, 
            node_color='skyblue', 
            node_size=1500, 
            font_size=12,
            font_weight='bold',
            edge_color='gray',
            width=2)
    
    # Salva e mostra a imagem
    plt.savefig('grafo_escolhido.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("\nGrafo gerado e salvo como 'grafo_escolhido.png'!\n")

def mostrar_grafo_escolhido(grafo):
    """
    Exibe o grafo diretamente com visualização interativa
    """
    nos = grafo.vertices
    arestas = grafo.arestas
    
    # Criação do grafo
    grafo = nx.Graph()
    
    # Adicionando elementos
    grafo.add_nodes_from(str(no) for no in nos)
    grafo.add_edges_from((str(a), str(b)) for a, b in arestas)
    
    # Configuração do gráfico
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(grafo, seed=42)  # Layout consistente
    
    # Desenho do grafo
    nx.draw(grafo, pos, with_labels=True,
            node_color='lightgreen',
            node_size=1200,
            font_size=10,
            font_weight='bold',
            edge_color='darkgray',
            width=2,
            alpha=0.8)
    
    # Adicionando título
    plt.title("Grafo Escolhido", fontsize=14, pad=20)
    
    # Exibindo o gráfico
    plt.show()

def exibir_menu():
    os.system("cls")
    print("╔═════════════════════════════════════════════════════════════════════╗")
    print("║   1 - Apresentar Grafo (representação gráfica)                      ║")
    print("╠═════════════════════════════════════════════════════════════════════╣")
    print("║   2 - Apresentar Árvore de Busca em Profundidade                    ║")
    print("╠═════════════════════════════════════════════════════════════════════╣")
    print("║   3 - Apresentar Tabela Lowpt(v) e G(v)                             ║")
    print("╠═════════════════════════════════════════════════════════════════════╣")
    print("║   4 - Listar Articulações com seus Respectivos Demarcadores         ║")
    print("╠═════════════════════════════════════════════════════════════════════╣")
    print("║   5 - Apresentar Componentes Biconexas e onde estão enraizadas (Tw) ║")
    print("╠═════════════════════════════════════════════════════════════════════╣")
    print("║   6 - Salvar Grafo                                                  ║")
    print("╠═════════════════════════════════════════════════════════════════════╣")
    print("║   7 - Sair                                                          ║")
    print("╚═════════════════════════════════════════════════════════════════════╝")

def acao_menu(opcao, grafo):
    global ultimaArvore 

    match opcao:
        case 1:
            os.system("cls")
            print(grafo)
            mostrar_grafo_escolhido(grafo)
            input("Aperte Enter para voltar ao menu. ")
            os.system("cls")
            return True
        
        case 2:
            os.system("cls")
            grafo.verticesDisponiveis()

            raiz = input("Escolha o vertice raiz de busca: ")
            ultimaArvore = busca_em_profundidade(grafo, raiz)

            print("\nÁrvore de busca em profundidade:\n")
            print(ultimaArvore)

            plotar_arvore(ultimaArvore)

            input("Aperte Enter para voltar ao menu. ")
            os.system("cls")
            return True

        case 3:
            os.system("cls")
            if(ultimaArvore == None):
                print("Você precisa gerar uma árvore de busca primeiro!")
                time.sleep(3)
                return True
            
            lowpt, g = calcular_lowpt_e_g(ultimaArvore)
            imprimir_lowpt_e_g(lowpt, g)    
            plotar_tabelas_lowpt_e_g(lowpt, g)
            return True

        case 4:  
            os.system("cls")
            if(ultimaArvore == None):
                print("Você precisa gerar uma árvore de busca primeiro!")
                time.sleep(3)
                return True
            
            print("\n\nArticulações → Demarcadores")
            dics = demarcadores_por_articulacao(ultimaArvore)
            for art, dms in dics.items():
                print(f"{art} → {dms}")

            input("\n\nAperte Enter para voltar ao menu. ")
            os.system("cls")
            return True

        case 5:
            os.system("cls")
            if(ultimaArvore == None):
                print("Você precisa gerar uma árvore de busca primeiro!")
                time.sleep(3)
                return True
            
            dem = demarcadores_por_articulacao(ultimaArvore)
            componentes = componentes_biconexas(grafo, ultimaArvore, dem)

            print("\n== Componentes Biconexas ==\n")
            for i, comp in enumerate(componentes, 1):
                print(f"Componente {i}:")
                print(f"  Articulação: {comp['articulacao']}")
                print(f"  Demarcador : {comp['raiz']}")
                print(f"  Vértices   : {sorted(comp['vertices'])}\n")

            input("\n\nAperte Enter para voltar ao menu. ")
            os.system("cls")
            return True

        case 6:
            os.system("cls")
            salvar_grafo_estatico(grafo)
            print("Imagem salva com: 'grafo_escolhido.png'")
            time.sleep(2) 
            os.system("cls")
            return True
        
        case 7:
            os.system("cls")
            return False
        case _:      
            os.system("cls")
            print("Opção inválida")
            time.sleep(2)
            os.system("cls")
            return True 

def invocar_menu(grafo):

    continarExecutando = True

    while continarExecutando:
        exibir_menu()
        print(f"\n {'='*20}\n")
        escolhaMenu = int(input("Insira a ação que deseja >> "))
        continarExecutando = acao_menu(escolhaMenu, grafo)