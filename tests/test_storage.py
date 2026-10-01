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

            numero = arquivo.aloca()
            pagina = Page(numero)
            pagina.escreve(b"MiniDB")

            arquivo.escreve_pagina(numero, pagina.le())

            pagina_lida = arquivo.le_pagina(numero)

            self.assertEqual(pagina_lida.numero, numero)
            self.assertEqual(pagina_lida.le()[:6], b"MiniDB")
            self.assertEqual(len(pagina_lida.le()), PAGE_SIZE)


if __name__ == "__main__":
    unittest.main()
