import unittest

from buffer.arvore_b_plus import ArvoreBPlus


class TestArvoreBPlus(unittest.TestCase):
    def test_insercao_e_busca(self):
        arvore = ArvoreBPlus(ordem=3)
        dados = [
            (10, "User10"),
            (20, "User20"),
            (5, "User5"),
            (30, "User30"),
            (25, "User25"),
            (40, "User40"),
            (15, "User15"),
            (35, "User35"),
            (45, "User45"),
            (50, "User50"),
            (55, "User55"),
        ]

        for chave, valor in dados:
            arvore.inserir(chave, valor)

        for chave, valor in dados:
            self.assertEqual(arvore.buscar(chave), valor)

        self.assertIsNone(arvore.buscar(99))

    def test_divisao_da_raiz(self):
        arvore = ArvoreBPlus(ordem=3)
        arvore.inserir(10, "User10")
        arvore.inserir(20, "User20")
        arvore.inserir(30, "User30")

        self.assertFalse(arvore.raiz.eh_folha)
        self.assertEqual(len(arvore.raiz.filhos), 2)
        self.assertEqual(arvore.raiz.chaves, [30])

    def test_divisoes_de_nos_internos_e_buscas(self):
        arvore = ArvoreBPlus(ordem=3)
        chaves = list(range(1, 61))

        for chave in chaves:
            arvore.inserir(chave, f"User{chave}")

        # A raiz precisa ter filhos internos depois de várias divisões.
        self.assertFalse(arvore.raiz.eh_folha)
        self.assertTrue(any(not filho.eh_folha for filho in arvore.raiz.filhos))

        for chave in chaves:
            self.assertEqual(arvore.buscar(chave), f"User{chave}")

        self.assertIsNone(arvore.buscar(0))
        self.assertIsNone(arvore.buscar(61))

    def test_folhas_encadeadas_em_ordem(self):
        arvore = ArvoreBPlus(ordem=3)
        chaves = [40, 10, 30, 20, 60, 50, 70, 80, 90, 0]

        for chave in chaves:
            arvore.inserir(chave, f"User{chave}")

        atual = arvore.raiz
        while not atual.eh_folha:
            atual = atual.filhos[0]

        chaves_nas_folhas = []
        while atual is not None:
            self.assertEqual(atual.chaves, sorted(atual.chaves))
            chaves_nas_folhas.extend(atual.chaves)
            atual = atual.proximo

        self.assertEqual(chaves_nas_folhas, sorted(chaves))

    def test_inserir_chave_existente_atualiza_valor(self):
        arvore = ArvoreBPlus(ordem=3)
        arvore.inserir(10, "valor antigo")
        arvore.inserir(10, "valor atualizado")

        self.assertEqual(arvore.buscar(10), "valor atualizado")
        self.assertEqual(arvore.raiz.chaves, [10])
        self.assertEqual(len(arvore.raiz.valores), 1)


if __name__ == "__main__":
    unittest.main()
