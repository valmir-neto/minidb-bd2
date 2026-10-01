import os
import tempfile
import unittest

from storage.data_file import DataFile
from storage.page import PAGE_SIZE, Page


class TestArmazenamento(unittest.TestCase):
    def test_escrever_e_ler_pagina(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)

            pagina = Page(0)
            pagina.escreve(b"MiniDB")

            arquivo.write_page(0, pagina.le())

            pagina_lida = arquivo.read_page(0)

            self.assertIsNotNone(pagina_lida)
            self.assertEqual(pagina_lida.page_id, 0)
            self.assertEqual(pagina_lida.read()[:6], b"MiniDB")
            self.assertEqual(len(pagina_lida.read()), PAGE_SIZE)


if __name__ == "__main__":
    unittest.main()
