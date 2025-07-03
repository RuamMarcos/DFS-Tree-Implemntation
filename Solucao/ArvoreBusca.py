from Grafo import Grafo

class ArvoreBusca:
    def __init__(self):
        self.arestas = []

    def adicionar_aresta(self, origem, destino, tipo):
        self.arestas.append(Aresta(origem, destino, tipo))

    def __repr__(self):
        return "\n".join(str(a) for a in self.arestas)
    
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
    arvore = ArvoreBusca()

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


