from .page import PAGE_SIZE


class DataFile:
    def __init__(self, filename):
        self.filename = filename
        open(self.filename, "ab").close()

    def write_page(self, page_id, data):
        if len(data) != PAGE_SIZE:
            raise ValueError("A página deve possuir exatamente 4096 bytes")

        with open(self.filename, "r+b") as file:
            file.seek(page_id * PAGE_SIZE)
            file.write(data)

    def read_page(self, page_id):
        with open(self.filename, "rb") as file:
            file.seek(page_id * PAGE_SIZE)
            data = file.read(PAGE_SIZE)

            if len(data) == 0:
                return None

            if len(data) != PAGE_SIZE:
                raise ValueError("Página incompleta encontrada no arquivo")

            return data
