PAGE_SIZE = 4096


class Page:
    def __init__(self, page_id):
        self.page_id = page_id
        self.data = bytearray(PAGE_SIZE)
        self.dirty = False

    def read(self):
        return bytes(self.data)

    def write(self, data):
        if len(data) > PAGE_SIZE:
            raise ValueError("Os dados excedem o tamanho da página")

        self.data[:len(data)] = data
        self.dirty = True
