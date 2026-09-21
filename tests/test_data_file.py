import os
import tempfile 
import unittest

from storage.data_file import DataFile
from storage.page import PAGE_SIZE, Page


class TestDataFile(unittest.TestCase):  #classe reponsavél por testar o DataFile
    def test_page_persistence(self): #verifica se a pagina continua persistente
        with tempfile.TemporaryDirectory() as directory: #cria uma pasta temporária
            filename = os.path.join(directory, "dados.db") #serve para montar o caminho do arquivo corretamente.
            arquivo = DataFile(filename) 
            pagina = Page(2)
            pagina.write(b"MiniDB") #esta sendo representando como bytes "b"

            arquivo.write_page(pagina.page_id, pagina.read()) #pega os dados da pag e grava no arquivo dados.db 
            pagina_lida = arquivo.read_page(2) #testa se aquilo que foi gravado pode ser recuperado.

            self.assertIsNotNone(pagina_lida) #verifica se a pag existe
            self.assertEqual(pagina_lida.page_id, 2) #confere o id da pag
            self.assertEqual(pagina_lida.read()[:6], b"MiniDB") #verifica se os 6 bytes estão iguais ao miniDB 
            self.assertEqual(len(pagina_lida.read()), PAGE_SIZE) #verifica se o tamanho da pag = 4096

    def test_page_count(self): #tesa quantas paginas existem
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "dados.db")
            arquivo = DataFile(filename)

            self.assertEqual(arquivo.page_count(), 0)

            arquivo.write_page(0, Page(0).read())
            arquivo.write_page(1, Page(1).read())

            self.assertEqual(arquivo.page_count(), 2)


if __name__ == "__main__":
    unittest.main()
