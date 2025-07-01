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
    
    def __str__(self):
        vertices_str = ', '.join(self.vertices)
        arestas_str = ',\n'.join([f'    {aresta}' for aresta in self.arestas])
        return f"V = [{vertices_str}]\nE = [\n{arestas_str}\n]"