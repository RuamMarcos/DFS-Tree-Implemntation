
def exibir_opcoes_matrizes(quantidade):
    # Cria a matriz automaticamente: ["matriz 1", "matriz 2", ...]
    matriz_opcoes = [f"matriz {i+1}" for i in range(quantidade)]
    
    # Define o título e calcula a largura da caixa
    titulo = "matrizes Carregadas"
    maior_comprimento = len(f"matriz {quantidade}")  # Maior texto possível
    largura_caixa = max(maior_comprimento + 8, len(titulo) + 4)
    
    # Cabeçalho
    print(f"╔{'═' * (largura_caixa - 2)}╗")
    print(f"║{titulo:^{largura_caixa - 2}}║")
    print(f"╠{'═' * (largura_caixa - 2)}╣")
    
    # Itens
    for i in range(quantidade):
        prefixo = "╟──" if i < quantidade - 1 else "╚──"
        item = f"matriz {i+1}"
        print(f"{prefixo} {item.ljust(largura_caixa - 8)}║")
    
    # Rodapé (só se houver itens)
    if quantidade > 0:
        print(f"╚{'═' * (largura_caixa - 2)}╝")