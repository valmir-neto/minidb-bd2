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
        
    def test_expulsao_pagina_nao_fixa(self):
        arquivo = DataFile("teste_cache.db")
        cache = Cache(arquivo, capacidade=3)
        
        arquivo.aloca()
        arquivo.aloca()
        arquivo.aloca()
        arquivo.aloca()
        
        cache.fixa(1)
        cache.solta(1)
        
        cache.fixa(2)
        cache.solta(2)
        
        cache.fixa(3)
        cache.solta(3)
        
        #a página 1 passa a ser mais recente usada
        cache.fixa(1)
        cache.solta(1)
        
        #o cache está cheio.
        #a página 2 é a menos recentemente usada.
        cache.fixa(4)
        cache.solta(4)

        self.assertNotIn(2, cache.frames)
        self.assertIn(1, cache.frames)
        self.assertIn(3, cache.frames)
        self.assertIn(4, cache.frames)
    
    
    def test_pagina_suja_e_gravada_ao_expulsar(self):
        arquivo = DataFile("teste_cache.db")

        arquivo.aloca()
        arquivo.aloca()

        cache = Cache(arquivo, capacidade=1)

        pagina = cache.fixa(1)

        pagina.escreve(b"MiniDB")

        cache.solta(1, sujou=True)

        #ao carregar a página 2, a página 1 precisa ser expulsa.
        arquivo.aloca()
        cache.fixa(2)

        arquivo_novo = DataFile("teste_cache.db")
        pagina_lida = arquivo_novo.le_pagina(1)

        self.assertEqual(pagina_lida.le()[:6], b"MiniDB")
        
if __name__ == "__main__":
    unittest.main()