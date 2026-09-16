from storage.data_file import DataFile
from storage.page import Page


def main():
    arquivo = DataFile("dados.db")
    pagina = Page(0)

    pagina.write(b"MiniDB funcionando!")
    arquivo.write_page(pagina.page_id, pagina.read())

    dados = arquivo.read_page(0)
    print(dados[:20])


if __name__ == "__main__":
    main()
