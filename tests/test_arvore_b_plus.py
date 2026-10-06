import unittest

from arvore.arvore_b_plus import ArvoreBPlus


class TestArvoreBPlus(unittest.TestCase):

    def test_insercao_e_busca(self):
        arvore = ArvoreBPlus(ordem=3)

        dados = [(10, "User10"),(20, "User20"),(5, "User5"),(30, "User30"),
                 (25, "User25"),(40, "User40"),(15, "User15"),(35, "User35"),
                 (45, "User45"),(50, "User50"),(55, "User55"),]

        for chave, valor in dados:
            arvore.inserir(chave, valor)

        self.assertEqual(arvore.buscar(15), "User15")
        self.assertEqual(arvore.buscar(55), "User55")
        self.assertIsNone(arvore.buscar(99))


if __name__ == "__main__":
    unittest.main()