from buffer.arvore_b_plus import ArvoreBPlus


def demonstrar_crescimento():
    arvore = ArvoreBPlus(ordem=3)
    chaves = [10, 20, 5, 30, 25, 40, 15, 35, 45, 50, 55]

    print("=== Inserção e crescimento da Árvore B+ ===")
    for chave in chaves:
        arvore.inserir(chave, f"User{chave}")
        print(f"\nApós inserir {chave}:")
        arvore.imprimir_arvore()

    return arvore


def demonstrar_buscas(arvore):
    print("\n=== Demonstração de buscas ===")
    for chave in (15, 55, 99):
        print(f"Buscar {chave}: {arvore.buscar(chave)!r}")


def demonstrar_folhas_encadeadas(arvore):
    print("\n=== Percurso das folhas encadeadas ===")
    atual = arvore.raiz

    while not atual.eh_folha:
        atual = atual.filhos[0]

    chaves = []
    while atual is not None:
        print(atual.chaves)
        chaves.extend(atual.chaves)
        atual = atual.proximo

    print("Chaves em ordem:", chaves)


if __name__ == "__main__":
    arvore = demonstrar_crescimento()
    demonstrar_buscas(arvore)
    demonstrar_folhas_encadeadas(arvore)
