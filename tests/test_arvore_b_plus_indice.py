import os
import tempfile
import unittest

from storage.page import PAGE_SIZE
from buffer.arvore_b_plus_indice import ArvoreBPlusIndice, No
from buffer.cache import Cache
from storage.data_file import DataFile



class TestArvoreBPlusIndice(unittest.TestCase):
    def setUp(self):
        self.arvore = ArvoreBPlusIndice(cache=None, ordem=3)

    def test_serializar_e_desserializar_folha(self):
        no = No(eh_folha=True)
        no.chaves = [10, 20]
        no.valores = [(1, 0), (2, 3)]
        no.proximo = 5
        
        dados = self.arvore.serializar_no(no)
        recuperado = self.arvore.desserializar_no(dados)

        self.assertEqual(len(dados), PAGE_SIZE)
        self.assertTrue(recuperado.eh_folha)
        self.assertEqual(recuperado.chaves, [10, 20])
        self.assertEqual(recuperado.valores, [(1, 0), (2, 3)])
        self.assertEqual(recuperado.proximo, 5)

    def test_serializar_e_desserializar_folha_sem_proxima(self):
        no = No(eh_folha=True)
        no.chaves = [30]
        no.valores = [(4, 2)]

        dados = self.arvore.serializar_no(no)
        recuperado = self.arvore.desserializar_no(dados)

        self.assertEqual(recuperado.chaves, [30])
        self.assertEqual(recuperado.valores, [(4, 2)])
        self.assertIsNone(recuperado.proximo)

    def test_serializar_e_desserializar_no_interno(self):
        no = No(eh_folha=False)
        no.chaves = [20, 40]
        no.filhos = [1, 2, 3]

        dados = self.arvore.serializar_no(no)
        recuperado = self.arvore.desserializar_no(dados)

        self.assertFalse(recuperado.eh_folha)
        self.assertEqual(recuperado.chaves, [20, 40])
        self.assertEqual(recuperado.filhos, [1, 2, 3])

    def test_salvar_e_carregar_no_com_cache(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=4)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            numero_pagina = arquivo.aloca()

            no = No(eh_folha=True)
            no.chaves = [10, 20]
            no.valores = [(1, 0), (2, 3)]
            no.proximo = None

            arvore.salvar_no(numero_pagina, no)
            cache.descarrega()

            recuperado = arvore.carregar_no(numero_pagina)

            self.assertEqual(recuperado.chaves, [10, 20])
            self.assertEqual(recuperado.valores, [(1, 0), (2, 3)])
            self.assertIsNone(recuperado.proximo)

            cache.descarrega()
    
    def test_persistencia_apos_reabrir_arquivo(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")

            # Cria o arquivo e salva o nó.
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=4)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            numero_pagina = arquivo.aloca()

            no = No(eh_folha=True)
            no.chaves = [15, 25]
            no.valores = [(2, 1), (3, 4)]
            no.proximo = None

            arvore.salvar_no(numero_pagina, no)
            cache.descarrega()

            # Descarta os objetos antigos e reabre o arquivo.
            del arvore
            del cache
            del arquivo

            arquivo_reaberto = DataFile(nome_arquivo)
            cache_novo = Cache(arquivo_reaberto, capacidade=4)
            arvore_nova = ArvoreBPlusIndice(
                cache=cache_novo,
                ordem=3
            )

            recuperado = arvore_nova.carregar_no(numero_pagina)

            self.assertTrue(recuperado.eh_folha)
            self.assertEqual(recuperado.chaves, [15, 25])
            self.assertEqual(recuperado.valores, [(2, 1), (3, 4)])
            self.assertIsNone(recuperado.proximo)

            cache_novo.descarrega()
        
    def test_raiz_persistente_apos_reabrir_arquivo(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")

            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=4)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            arvore.inicializar_indice()
            numero_raiz = arvore.raiz

            del arvore
            del cache
            del arquivo

            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=4)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            raiz_recuperada = arvore.carregar_metadados()
            no_raiz = arvore.carregar_no(raiz_recuperada)

            self.assertEqual(raiz_recuperada, numero_raiz)
            self.assertTrue(no_raiz.eh_folha)
            self.assertEqual(no_raiz.chaves, [])

            cache.descarrega()

    def test_buscar_chave_na_folha(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=4)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            arvore.inicializar_indice()

            no = No(eh_folha=True)
            no.chaves = [10, 20, 30]
            no.valores = [(3, 0), (4, 1), (5, 2)]

            arvore.salvar_no(arvore.raiz, no)

            self.assertEqual(arvore.buscar(10), (3, 0))
            self.assertEqual(arvore.buscar(20), (4, 1))
            self.assertEqual(arvore.buscar(30), (5, 2))
            self.assertIsNone(arvore.buscar(15))
            self.assertIsNone(arvore.buscar(40))

            cache.descarrega()

    
    def test_inserir_chaves_na_folha(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=4)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            arvore.inicializar_indice()

            arvore.inserir(10, (1, 0))
            arvore.inserir(20, (2, 1))
            arvore.inserir(30, (3, 2))

            self.assertEqual(arvore.buscar(10), (1, 0))
            self.assertEqual(arvore.buscar(20), (2, 1))
            self.assertEqual(arvore.buscar(30), (3, 2))

            cache.descarrega()
        
        
    def test_divisao_de_nos_em_varios_niveis(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=8)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)

            arvore.inicializar_indice()

            # Inserir em ordem crescente provoca várias divisões.
            quantidade = 30

            for chave in range(1, quantidade + 1):
                arvore.inserir(chave, (chave + 100, chave))

            # A raiz deve ser interna após as divisões.
            raiz = arvore.carregar_no(arvore.raiz)
            self.assertFalse(raiz.eh_folha)

            # Deve existir pelo menos um nó interno abaixo da raiz.
            encontrou_no_interno = False

            for numero_filho in raiz.filhos:
                filho = arvore.carregar_no(numero_filho)

                if not filho.eh_folha:
                    encontrou_no_interno = True
                    break

            self.assertTrue(
                encontrou_no_interno,
                "A árvore deveria ter mais de um nível de nós internos."
            )

            # Todas as chaves devem continuar sendo encontradas.
            for chave in range(1, quantidade + 1):
                esperado = (chave + 100, chave)
                self.assertEqual(arvore.buscar(chave), esperado)

            # Chaves que não foram inseridas não devem ser encontradas.
            self.assertIsNone(arvore.buscar(0))
            self.assertIsNone(arvore.buscar(31))

            cache.descarrega()
        
        
    def test_persistencia_apos_divisoes(self):
        with tempfile.TemporaryDirectory() as diretorio:
            nome_arquivo = os.path.join(diretorio, "indice.db")

        # Cria o índice e insere várias chaves.
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=8)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)
    
            arvore.inicializar_indice()
    
            quantidade = 30
    
            for chave in range(1, quantidade + 1):
                arvore.inserir(chave, (chave + 100, chave))
    
            raiz_original = arvore.raiz
            cache.descarrega()
    
            # Descarta os objetos para simular a reabertura.
            del arvore
            del cache
            del arquivo
    
            # Reabre o mesmo arquivo e recupera a raiz.
            arquivo = DataFile(nome_arquivo)
            cache = Cache(arquivo, capacidade=8)
            arvore = ArvoreBPlusIndice(cache=cache, ordem=3)
    
            raiz_recuperada = arvore.carregar_metadados()
    
            self.assertEqual(raiz_recuperada, raiz_original)
    
            # Verifica se todas as chaves e RIDs persistiram.
            for chave in range(1, quantidade + 1):
                esperado = (chave + 100, chave)
                self.assertEqual(arvore.buscar(chave), esperado)
    
            self.assertIsNone(arvore.buscar(0))
            self.assertIsNone(arvore.buscar(31))
    
            cache.descarrega()
    




if __name__ == "__main__":
    unittest.main()
