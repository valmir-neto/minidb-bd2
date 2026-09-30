INT_SIZE = 4


class FixedRecord:
    """Representa um registro composto somente por inteiros de 4 bytes."""

    def __init__(self, values):
        self.values = tuple(values)

    @property
    def size(self):
        return len(self.values) * INT_SIZE

    def serialize(self):
        data = bytearray()

        for value in self.values:
            data.extend(int(value).to_bytes(INT_SIZE, byteorder="little", signed=True))

        return bytes(data)

    @classmethod
    def deserialize(cls, data):
        if len(data) % INT_SIZE != 0:
            raise ValueError("Tamanho de registro inválido")

        values = []

        for position in range(0, len(data), INT_SIZE):
            value = int.from_bytes(
                data[position:position + INT_SIZE],
                byteorder="little",
                signed=True,
            )
            values.append(value)

        return cls(values)
