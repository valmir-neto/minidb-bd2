import os
import tempfile
import unittest

from storage.data_file import DataFile
from storage.page import PAGE_SIZE, Page


class TestStorage(unittest.TestCase):
    def test_page_write_and_read(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "dados.db")
            arquivo = DataFile(filename)

            pagina = Page(0)
            pagina.write(b"MiniDB")

            arquivo.write_page(0, pagina.read())

            pagina_lida = arquivo.read_page(0)

            self.assertIsNotNone(pagina_lida)
            self.assertEqual(pagina_lida.page_id, 0)
            self.assertEqual(pagina_lida.read()[:6], b"MiniDB")
            self.assertEqual(len(pagina_lida.read()), PAGE_SIZE)


if __name__ == "__main__":
    unittest.main()
