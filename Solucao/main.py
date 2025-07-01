from Auxiliares import *
from Grafo import  Grafo

grafos = ler_grafos("grafo.txt")
grafo = escolher_grafo(grafos)

salvar_grafo_estatico(grafo)
mostrar_grafo_escolhido(grafo)