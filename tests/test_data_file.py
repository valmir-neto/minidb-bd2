import os
import tempfile

from storage.data_file import DataFile
from storage.page import PAGE_SIZE, Page


def test_page_persistence():
    with tempfile.TemporaryDirectory() as directory:
        filename = os.path.join(directory, "dados.db")
        arquivo = DataFile(filename)
        pagina = Page(2)
        pagina.write(b"MiniDB")

        arquivo.write_page(pagina.page_id, pagina.read())

        pagina_lida = arquivo.read_page(2)

        assert pagina_lida is not None
        assert pagina_lida.page_id == 2
        assert pagina_lida.read()[:6] == b"MiniDB"
        assert len(pagina_lida.read()) == PAGE_SIZE


def test_page_count():
    with tempfile.TemporaryDirectory() as directory:
        filename = os.path.join(directory, "dados.db")
        arquivo = DataFile(filename)

        assert arquivo.page_count() == 0

        arquivo.write_page(0, Page(0).read())
        arquivo.write_page(1, Page(1).read())

        assert arquivo.page_count() == 2


if __name__ == "__main__":
    test_page_persistence()
    test_page_count()
    print("Testes do arquivo de dados: OK")
