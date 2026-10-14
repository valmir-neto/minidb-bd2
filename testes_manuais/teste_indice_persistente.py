
import os
import tempfile

from buffer.arvore_b_plus_indice import ArvoreBPlusIndice
from buffer.cache import Cache
from storage.data_file import DataFile


def demonstrar_persistencia():
    with tempfile.TemporaryDirectory() as diretorio:
        nome_arquivo = os.path.join(diretorio, "indice.db")

        print("Criando o índice B+ ")

        arquivo = DataFile(nome_arquivo)
        cache = Cache(arquivo, capacidade=8)
        arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

        arvore.inicializar_indice()

        # Insere chaves para provocar divisões na árvore.
        # quantidade = int(input("Digite a quantidade de chaves a serem inseridas: "))

        quantidade = 30

        for chave in range(1, quantidade + 1):
            rid = (chave + 100, chave)
            arvore.inserir(chave, rid)
        cache.descarrega()

        raiz_original = arvore.raiz

        print(f"Chaves inseridas: {quantidade}")
        print(f"Página da raiz antes de reabrir: {raiz_original}")

        # Descarta os objetos usados na primeira abertura.
        del arvore
        del cache
        del arquivo

        print("\n=== Reabrindo o arquivo ===")

        arquivo = DataFile(nome_arquivo)
        cache = Cache(arquivo, capacidade=8)
        arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

        raiz_recuperada = arvore.carregar_metadados()

        print(f"Página da raiz recuperada: {raiz_recuperada}")

        # Confere se todas as chaves continuam disponíveis.
        for chave in range(1, quantidade + 1):
            esperado = (chave + 100, chave) 
            encontrado = arvore.buscar(chave)

            if encontrado != esperado:
                raise AssertionError(
                    f"Erro na chave {chave}: "
                    f"esperado {esperado}, encontrado {encontrado}"
                )

        # Confere buscas por chaves inexistentes.
        assert arvore.buscar(0) is None
        assert arvore.buscar(quantidade + 1) is None

        print(f"Todas as {quantidade} chaves foram recuperadas corretamente.")
        print("As buscas por chaves inexistentes retornaram None.")
        print("Teste de persistência concluído com sucesso!")

        cache.descarrega()


if __name__ == "__main__":
    demonstrar_persistencia()
