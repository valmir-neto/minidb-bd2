import unittest

from buffer.cache import Cache
from storage.data_file import DataFile


class TestCache(unittest.TestCase):
    def test_mesma_pagina_gera_acerto(self):
        arquivo = DataFile("teste_cache.db")
        cache = Cache(arquivo, capacidade=3)

        arquivo.aloca()
        

        cache.fixa(1)
        cache.solta(1)

        cache.fixa(1)
        cache.solta(1)

        self.assertEqual(cache.acertos, 1)
        self.assertEqual(cache.faltas, 1)
        
if __name__ == "__main__":
    unittest.main()