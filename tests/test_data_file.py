import os
import tempfile
import unittest

from storage.data_file import DataFile
from storage.page import PAGE_SIZE
from storage.record import FixedRecord


class TestArquivoDados(unittest.TestCase):
    def test_criacao_do_arquivo(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)

            self.assertEqual(arquivo.page_count(), 1)
            self.assertEqual(os.path.getsize(nome_arquivo), PAGE_SIZE)

    def test_alocacao_de_pagina(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)

            numero = arquivo.aloca()

            self.assertEqual(numero, 1)
            self.assertEqual(arquivo.page_count(), 2)
            self.assertEqual(os.path.getsize(nome_arquivo), PAGE_SIZE * 2)

    def test_insercao_e_rid(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)
            registro = FixedRecord((1, 20260001))

            rid = arquivo.insere(registro)

            self.assertEqual(rid, (1, 0))

            pagina = arquivo.le_pagina(rid[0])
            dados = pagina.le_registro(rid[1], registro.tamanho)
            restaurado = FixedRecord.desserializa(dados)

            self.assertEqual(restaurado.valores, (1, 20260001))

    def test_persistencia_apos_reabrir(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "dados.db")
            arquivo = DataFile(nome_arquivo)
            registro = FixedRecord((1, 20260001))

            rid = arquivo.insere(registro)
            arquivo.sync()

            arquivo = DataFile(nome_arquivo)
            pagina = arquivo.le_pagina(rid[0])
            dados = pagina.le_registro(rid[1], registro.tamanho)
            restaurado = FixedRecord.desserializa(dados)

            self.assertEqual(restaurado.valores, (1, 20260001))


if __name__ == "__main__":
    unittest.main()
