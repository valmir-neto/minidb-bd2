import unittest

from storage.page import PAGE_SIZE, CABECALHO_SIZE, Page
from storage.record import FixedRecord


class TestPagina(unittest.TestCase):
    def test_tamanho_da_pagina(self):
        pagina = Page(1)

        self.assertEqual(len(pagina.le()), PAGE_SIZE)

    def test_cabecalho_da_pagina(self):
        pagina = Page(1)

        self.assertEqual(CABECALHO_SIZE, 16)
        self.assertEqual(pagina.quantidade_registros(), 0)

    def test_capacidade_de_registros(self):
        pagina = Page(1)
        registro = FixedRecord((1, 20260001))

        self.assertEqual(registro.tamanho, 8)
        self.assertEqual(pagina.capacidade(registro.tamanho), 510)

    def test_adicionar_e_ler_registro(self):
        pagina = Page(1)
        registro = FixedRecord((1, 20260001))
        dados = registro.serializa()

        slot = pagina.insere_registro(dados)

        self.assertEqual(slot, 0)
        self.assertEqual(pagina.quantidade_registros(), 1)
        self.assertEqual(pagina.le_registro(0, registro.tamanho), dados)


if __name__ == "__main__":
    unittest.main()
