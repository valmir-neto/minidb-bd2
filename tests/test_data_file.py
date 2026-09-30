import os
import tempfile
import unittest

from storage.data_file import DataFile
from storage.page import PAGE_SIZE, Page


class TestArquivoDados(unittest.TestCase):
    def test_persistencia_da_pagina(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)
            pagina = Page(2)
            pagina.write(b"MiniDB")

            arquivo.write_page(pagina.page_id, pagina.read())
            pagina_lida = arquivo.read_page(2)

            self.assertIsNotNone(pagina_lida)
            self.assertEqual(pagina_lida.page_id, 2)
            self.assertEqual(pagina_lida.read()[:6], b"MiniDB")
            self.assertEqual(len(pagina_lida.read()), PAGE_SIZE)

    def test_contagem_de_paginas(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)

            self.assertEqual(arquivo.page_count(), 0)

            arquivo.write_page(0, Page(0).read())
            arquivo.write_page(1, Page(1).read())

            self.assertEqual(arquivo.page_count(), 2)


if __name__ == "__main__":
    unittest.main()
