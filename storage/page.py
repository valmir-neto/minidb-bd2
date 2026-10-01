import struct

PAGE_SIZE = 4096
CABECALHO_SIZE = 16


class Page:
    def __init__(self, numero, dados=None):
        self.numero = numero
        self.dados = bytearray(PAGE_SIZE)

        if dados is not None:
            if len(dados) != PAGE_SIZE:
                raise ValueError("A página deve possuir exatamente 4096 bytes")
            self.dados[:] = dados

    def le(self):
        return bytes(self.dados)

    def escreve(self, dados):
        if len(dados) > PAGE_SIZE:
            raise ValueError("Os dados excedem o tamanho da página")

        self.dados[:] = bytearray(PAGE_SIZE)
        self.dados[:len(dados)] = dados

    def quantidade_registros(self):
        return struct.unpack("<I", self.dados[:4])[0]

    def capacidade(self, tamanho_registro):
        if tamanho_registro <= 0:
            raise ValueError("O tamanho do registro deve ser positivo")

        return (PAGE_SIZE - CABECALHO_SIZE) // tamanho_registro

    def insere_registro(self, dados):
        tamanho_registro = len(dados)

        if tamanho_registro == 0:
            raise ValueError("O registro não pode ser vazio")

        quantidade = self.quantidade_registros()

        if quantidade >= self.capacidade(tamanho_registro):
            raise ValueError("A página está cheia")

        deslocamento = CABECALHO_SIZE + quantidade * tamanho_registro
        self.dados[deslocamento:deslocamento + tamanho_registro] = dados
        self.dados[:4] = struct.pack("<I", quantidade + 1)

        return quantidade

    def le_registro(self, slot, tamanho_registro):
        quantidade = self.quantidade_registros()

        if slot < 0 or slot >= quantidade:
            raise IndexError("Slot inexistente na página")

        if tamanho_registro <= 0:
            raise ValueError("O tamanho do registro deve ser positivo")

        deslocamento = CABECALHO_SIZE + slot * tamanho_registro
        return bytes(self.dados[deslocamento:deslocamento + tamanho_registro])
