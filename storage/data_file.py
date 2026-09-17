from .page import PAGE_SIZE, Page


class DataFile:
    def __init__(self, filename):
        self.filename = filename
        open(self.filename, "ab").close()

    def write_page(self, page_id, data):
        if page_id < 0:
            raise ValueError("O identificador da página não pode ser negativo")

        if len(data) != PAGE_SIZE:
            raise ValueError("A página deve possuir exatamente 4096 bytes")

        with open(self.filename, "r+b") as file:
            file.seek(page_id * PAGE_SIZE)
            file.write(data)

    def read_page(self, page_id):
        if page_id < 0:
            raise ValueError("O identificador da página não pode ser negativo")

        with open(self.filename, "rb") as file:
            file.seek(page_id * PAGE_SIZE)
            data = file.read(PAGE_SIZE)

        if len(data) == 0:
            return None

        if len(data) != PAGE_SIZE:
            raise ValueError("Página incompleta encontrada no arquivo")

        return Page(page_id, data)

    def page_count(self):
        size = __import__("os").path.getsize(self.filename)
        if size % PAGE_SIZE != 0:
            raise ValueError("Arquivo de dados possui tamanho inválido")

        return size // PAGE_SIZE
