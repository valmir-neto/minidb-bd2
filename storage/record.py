INT_SIZE = 4


class FixedRecord:
    def __init__(self, valores):
        self.valores = tuple(valores)

    @property
    def tamanho(self):
        return len(self.valores) * INT_SIZE

    def serializa(self):
        dados = bytearray()

        for valor in self.valores:
            dados.extend(int(valor).to_bytes(INT_SIZE, byteorder="little", signed=True))

        return bytes(dados)

    @classmethod
    def desserializa(cls, dados):
        if len(dados) % INT_SIZE != 0:
            raise ValueError("Tamanho de registro inválido")

        valores = []

        for posicao in range(0, len(dados), INT_SIZE):
            valor = int.from_bytes(
                dados[posicao:posicao + INT_SIZE],
                byteorder="little",
                signed=True,
            )
            valores.append(valor)

        return cls(valores)
