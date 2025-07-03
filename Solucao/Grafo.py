class Grafo:
    def __init__(self, matriz_incidencia):
        self.vertices = []
        self.arestas = []
        
        # Determinar o número de vértices (tamanho da matriz)
        num_vertices = len(matriz_incidencia)
        
        # Criar os vértices v1, v2, ..., vn
        self.vertices = [f'v{i+1}' for i in range(num_vertices)]
        
        # Percorrer a matriz para encontrar as arestas
        for i in range(num_vertices):
            for j in range(i+1, num_vertices):  # Evitar duplicatas e laços
                if matriz_incidencia[i][j] == 1:
                    self.arestas.append([f'v{i+1}', f'v{j+1}'])

    def adjacentes(self, v):
        vizinhos = set()
        for a, b in self.arestas:
            if a == v:
                vizinhos.add(b)
            elif b == v:
                vizinhos.add(a)
        return list(vizinhos)
    
    def __str__(self):
        msg = ""
        msg += (f"{"-"*17}\nVértices do Grafo\n{"-"*17}\n")
        for vertice in self.vertices:
            msg += (f"\nVetice {self.vertices.index(vertice)}: {vertice}")
        msg += ("\n\n")

        msg += (f"{"-"*17}\nArestas do Grafo\n{"-"*17}\n")
        for aresta in self.arestas:
            msg += (f"\nAresta {self.arestas.index(aresta)}: {aresta}")
        msg += ("\n\n")

        return msg
    
    def verticesDisponiveis(self):
        msg = ""
        msg += (f"{"-"*17}\nVértices do Grafo\n{"-"*17}\n")
        for vertice in self.vertices:
            msg += (f"\nVetice {self.vertices.index(vertice)}: {vertice}")
        msg += ("\n\n")
        print(msg)