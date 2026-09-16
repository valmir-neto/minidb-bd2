from storage.data_file import DataFile
from storage.page import PAGE_SIZE


def test_page_write_and_read():
    filename = "test_dados.db"
    arquivo = DataFile(filename)
    conteudo = b"MiniDB"

    pagina = bytearray(PAGE_SIZE)
    pagina[:len(conteudo)] = conteudo
    arquivo.write_page(0, bytes(pagina))

    dados = arquivo.read_page(0)

    assert dados[:len(conteudo)] == conteudo
    assert len(dados) == PAGE_SIZE


if __name__ == "__main__":
    test_page_write_and_read()
    print("Teste do armazenamento: OK")
