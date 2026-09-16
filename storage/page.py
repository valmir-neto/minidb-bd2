import struct

PAGE_SIZE = 4096
HEADER_SIZE = 4


class Page:
    def __init__(self, page_id, data=None):
        self.page_id = page_id
        self.data = bytearray(PAGE_SIZE)
        self.dirty = False

        if data is not None:
            if len(data) != PAGE_SIZE:
                raise ValueError("A página deve possuir exatamente 4096 bytes")
            self.data[:] = data

    def read(self):
        return bytes(self.data)

    def write(self, data):
        if len(data) > PAGE_SIZE:
            raise ValueError("Os dados excedem o tamanho da página")

        self.data[:len(data)] = data
        self.dirty = True

    def record_count(self):
        return struct.unpack("<I", self.data[:HEADER_SIZE])[0]

    def capacity(self, record_size):
        if record_size <= 0:
            raise ValueError("O tamanho do registro deve ser positivo")

        return (PAGE_SIZE - HEADER_SIZE) // record_size

    def append_record(self, record_data):
        record_size = len(record_data)

        if record_size == 0:
            raise ValueError("O registro não pode ser vazio")

        count = self.record_count()
        if count >= self.capacity(record_size):
            raise ValueError("A página está cheia")

        offset = HEADER_SIZE + count * record_size
        self.data[offset:offset + record_size] = record_data
        self.data[:HEADER_SIZE] = struct.pack("<I", count + 1)
        self.dirty = True

        return count

    def get_record(self, record_number, record_size):
        count = self.record_count()

        if record_number < 0 or record_number >= count:
            raise IndexError("Registro inexistente na página")

        offset = HEADER_SIZE + record_number * record_size
        return bytes(self.data[offset:offset + record_size])
