from Grafo import Grafo
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.table import Table


class ArvoreBusca:
    def __init__(self, raiz=None):
        self.arestas = []
        self.raiz = raiz

    def adicionar_aresta(self, origem, destino, tipo):
        self.arestas.append(Aresta(origem, destino, tipo))

    def __repr__(self):
        info = f"Raiz: {self.raiz}\n"
        return info + "\n".join(str(a) for a in self.arestas)


  
class Aresta:
    def __init__(self, origem, destino, tipo):
        self.origem = origem
        self.destino = destino
        self.tipo = tipo  # "arvore" ou "retorno"

    def __repr__(self):
        return f"({self.origem} -> {self.destino}, tipo: {self.tipo})"

def busca_em_profundidade(grafo, raiz):
    visitado = {v: False for v in grafo.vertices}
    pilha = []
    arvore = ArvoreBusca(raiz=raiz)  # <-- raiz registrada aqui

    def dfs(v):
        visitado[v] = True
        pilha.append(v)

        for w in grafo.adjacentes(v):
            if not visitado[w]:
                arvore.adicionar_aresta(v, w, "arvore")
                dfs(w)
            elif w in pilha and (len(pilha) < 2 or w != pilha[-2]):
                arvore.adicionar_aresta(v, w, "retorno")

        pilha.pop()

    dfs(raiz)
    return arvore

def plotar_arvore(arvore):
    
   import networkx as nx
    import matplotlib.pyplot as plt
    from collections import deque, defaultdict

    G = nx.DiGraph()
    aresta_arvore = []
    aresta_retorno = []

    for a in arvore.arestas:
        G.add_node(a.origem)
        G.add_node(a.destino)
        if a.tipo == "arvore":
            aresta_arvore.append((a.origem, a.destino))
        elif a.tipo == "retorno":
            aresta_retorno.append((a.origem, a.destino))

    G_tree = nx.DiGraph()
    G_tree.add_edges_from(aresta_arvore)

    levels = {}
    children = defaultdict(list)
    for pai, filho in aresta_arvore:
        children[pai].append(filho)
    queue = deque([(arvore.raiz, 0)])
    while queue:
        node, level = queue.popleft()
        levels[node] = level
        for filho in children.get(node, []):
            queue.append((filho, level + 1))

    nivel_nos = defaultdict(list)
    for node, level in levels.items():
        nivel_nos[level].append(node)
    max_width = max(len(nos) for nos in nivel_nos.values())

    pos = {}
    for level, nos in nivel_nos.items():
        n = len(nos)
        for i, node in enumerate(sorted(nos)):
            pos[node] = ((i + 1) / (n + 1), -level)

    plt.figure(figsize=(max(8, 2*max_width), 6))

    nx.draw_networkx_edges(G, pos, edgelist=aresta_arvore, edge_color='black', width=2, arrows=False)


    for u, v in aresta_retorno:
        rad = 0.3
        if pos[u][1] < pos[v][1]:
            rad = -rad
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)],
            edge_color='red', width=2, arrows=True,
            connectionstyle=f'arc3,rad={rad}',
            arrowstyle='-'
        )

    nx.draw_networkx_nodes(G, pos, node_color='black', node_size=250)
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold', font_size=12)

    plt.axis('off')
    plt.title("Árvore de Busca em Profundidade", fontsize=15, pad=15)
    plt.tight_layout()
    plt.show()


def calcular_lowpt_e_g(arvore_busca):

    if not arvore_busca.raiz:
        raise ValueError("A árvore precisa ter uma raiz definida.")

    vertices = set()
    tree_edges = []   # arestas de árvore: pai → filho
    back_edges = []   # arestas de retorno: descendente → ancestral

    for a in arvore_busca.arestas:
        vertices.update([a.origem, a.destino])
        if a.tipo == "arvore":
            tree_edges.append((a.origem, a.destino))
        elif a.tipo == "retorno":
            back_edges.append((a.origem, a.destino))

    # ---------- Construir árvore ----------
    parent = {}
    children = {v: [] for v in vertices}

    for pai, filho in tree_edges:
        parent[filho] = pai
        children[pai].append(filho)

    # ---------- Numeração em pré-ordem ----------
    dfs_num = {}
    ordem = []

    def dfs_numera(v):
        dfs_num[v] = len(ordem)
        ordem.append(v)
        for f in children.get(v, []):
            dfs_numera(f)

    dfs_numera(arvore_busca.raiz)

    def mais_alto(u, v):  # retorna o mais próximo da raiz
        return u if dfs_num[u] < dfs_num[v] else v

    # ---------- Inicializar g(v) e lowpt(v) ----------
    lowpt = {v: v for v in vertices}
    g     = {v: v for v in vertices}

    # g(v): mais próximo da raiz alcançável só por arestas de retorno
    back_out = {}
    for u, anc in back_edges:
        back_out.setdefault(u, []).append(anc)

    for v in sorted(vertices, key=lambda x: dfs_num[x]):
        for anc in back_out.get(v, []):
            g[v] = mais_alto(g[v], g[anc])

    # lowpt(v): inicializa com retorno direto
    for u, anc in back_edges:
        lowpt[u] = mais_alto(lowpt[u], anc)

    # propaga lowpt para cima na árvore (pós-ordem)
    def propaga_lowpt(v):
        for filho in children.get(v, []):
            propaga_lowpt(filho)
            lowpt[v] = mais_alto(lowpt[v], lowpt[filho])

    propaga_lowpt(arvore_busca.raiz)

    lowpt["lowpt(vi)"] = "vi"
    g["g(vi)"] = "vi"
    lowptOrdenado = dict(sorted(lowpt.items()))
    gOrdenado = dict(sorted(g.items()))

    return lowptOrdenado, gOrdenado

def imprimir_lowpt_e_g(lowpt, g):
    for v in lowpt: print(f"  {v}: {lowpt[v]}")
    for v in g: print(f"  {v}: {g[v]}")

def plotar_tabelas_lowpt_e_g(dict1, dict2, title1="", title2=""):
    # Cria a figura com dois subplots (uma tabela em cima da outra)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4))
    fig.suptitle("Calculos de Lowpt e G(v)", fontsize=14, y=1.05)
    
    # Função auxiliar para plotar uma tabela a partir de um dicionário
    def plot_table(ax, dictionary, title):
        ax.set_title(title, pad=10, fontsize=12)
        ax.axis('off')
        
        # Extrai chaves e valores do dicionário
        keys = list(dictionary.keys())
        values = list(dictionary.values())
        
        # Cria a tabela
        table = Table(ax, bbox=[0, 0, 1, 1])
        
        # Adiciona as chaves (primeira linha)
        for col, key in enumerate(keys):
            table.add_cell(0, col, width=0.2, height=0.3, text=str(key), loc='center')
        
        # Adiciona os valores (segunda linha)
        for col, value in enumerate(values):
            table.add_cell(1, col, width=0.2, height=0.3, text=str(value), loc='center')
        
        ax.add_table(table)
    
    # Plota as duas tabelas
    plot_table(ax1, dict1, title1)
    plot_table(ax2, dict2, title2)
    
    plt.tight_layout()
    plt.show()

def demarcadores_por_articulacao(arvore):

    if not arvore.raiz:
        raise ValueError("Árvore precisa ter .raiz definida")

    # --- 1. lowpt ---
    lowpt, _ = calcular_lowpt_e_g(arvore)

    # --- 2. reconstruir relações pai‑filho (somente arestas‑árvore) ---
    filhos = {}
    pai    = {}
    for a in arvore.arestas:
        if a.tipo == "arvore":
            pai[a.destino] = a.origem
            filhos.setdefault(a.origem, []).append(a.destino)
            filhos.setdefault(a.destino, [])
        else:
            # garante vértices isolados em filhos
            filhos.setdefault(a.origem, [])
            filhos.setdefault(a.destino, [])

    # --- 3. percorrer a árvore em pós‑ordem para detectar demarcadores ---
    raiz = arvore.raiz
    demarcadores = {}          # resultado final

    def dfs(v):
        for f in filhos.get(v, []):
            dfs(f)

        if v == raiz:
            if len(filhos[v]) > 1:        # raiz com ≥2 filhos
                demarcadores[v] = filhos[v][:]
        else:
            for f in filhos.get(v, []):
                if lowpt[f] == v or lowpt[f] == f:
                    demarcadores.setdefault(v, []).append(f)

    dfs(raiz)
    return demarcadores

def componentes_biconexas(grafo, arvore, demarcadores):
    """
    Retorna lista de dicionários:
        [
          {
            'articulacao': v,
            'raiz': w,              # demarcador
            'vertices': { ... }     # Tw ∪ {v}
          },
          ...
        ]
    """
    if not arvore.raiz:
        raise ValueError("Árvore precisa ter .raiz definida")

    # --- 1. reconstruir pai → filhos (apenas arestas de árvore) 
    filhos = {}
    for a in arvore.arestas:
        if a.tipo == "arvore":
            filhos.setdefault(a.origem, []).append(a.destino)
            filhos.setdefault(a.destino, [])  # garante chave
        else:
            # para vértices sem filhos
            filhos.setdefault(a.origem, [])
            filhos.setdefault(a.destino, [])

    articulacoes = set(demarcadores.keys())

    # 2. função auxiliar para pegar Tw
    def coletar_subarvore(raiz_sub):
        """
        Retorna vértices da subárvore com raiz raiz_sub,
        parando antes de descer por vértices que sejam articulações.
        """
        stack = [raiz_sub]
        coletados = set()
        while stack:
            v = stack.pop()
            coletados.add(v)
            for f in filhos.get(v, []):
                if f not in articulacoes:      # não atravessa nova articulação
                    stack.append(f)
        return coletados

    #  3. montar componentes biconexas 
    componentes = []

    for v, ws in demarcadores.items():          # v = articulação, ws = lista de dem.
        for w in ws:
            comp = coletar_subarvore(w)
            comp.add(v)                         # Tw ∪ {v}
            componentes.append(
                {
                    "articulacao": v,
                    "raiz": w,
                    "vertices": comp,
                }
            )

    return componentes
