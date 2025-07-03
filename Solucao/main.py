from Auxiliares import *
from Grafo import  Grafo
import os

grafos = ler_grafos("grafo.txt")
grafo = escolher_grafo(grafos)

os.system("cls")

invocar_menu(grafo)

print("\n\n\nEncerrando execução...\n")