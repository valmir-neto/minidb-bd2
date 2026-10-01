import os
import struct

from .page import PAGE_SIZE, Page


NUMERO_MAGICO = b"MINIDB\x00\x00"
VERSAO_FORMATO = 1
DESLOCAMENTO_MAGICO = 0
DESLOCAMENTO_VERSAO = 8
DESLOCAMENTO_TAMANHO_PAGINA = 10
DESLOCAMENTO_TOTAL_PAGINAS = 14
DESLOCAMENTO_PRIMEIRA_PAGINA_LIVRE = 18


class DataFile:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

        if not os.path.exists(self.nome_arquivo):
            self._cria_arquivo()
        elif os.path.getsize(self.nome_arquivo) == 0:
            self._cria_arquivo()

        self._valida_arquivo()

    def _cria_arquivo(self):
        with open(self.nome_arquivo, "w+b") as arquivo:
            dados = bytearray(PAGE_SIZE)

            dados[DESLOCAMENTO_MAGICO:DESLOCAMENTO_MAGICO + 8] = NUMERO_MAGICO
            dados[DESLOCAMENTO_VERSAO:DESLOCAMENTO_VERSAO + 2] = struct.pack(
                "<H", VERSAO_FORMATO
            )
            dados[
                DESLOCAMENTO_TAMANHO_PAGINA:DESLOCAMENTO_TAMANHO_PAGINA + 4
            ] = struct.pack("<I", PAGE_SIZE)
            dados[
                DESLOCAMENTO_TOTAL_PAGINAS:DESLOCAMENTO_TOTAL_PAGINAS + 4
            ] = struct.pack("<I", 1)
            dados[
                DESLOCAMENTO_PRIMEIRA_PAGINA_LIVRE:
                DESLOCAMENTO_PRIMEIRA_PAGINA_LIVRE + 4
            ] = struct.pack("<I", 0)

            arquivo.write(dados)
            arquivo.flush()
            os.fsync(arquivo.fileno())

    def _valida_arquivo(self):
        tamanho_arquivo = os.path.getsize(self.nome_arquivo)

        if tamanho_arquivo < PAGE_SIZE:
            raise ValueError("Arquivo de dados inválido")

        if tamanho_arquivo % PAGE_SIZE != 0:
            raise ValueError("Arquivo de dados está corrompido")

        with open(self.nome_arquivo, "rb") as arquivo:
            dados = arquivo.read(PAGE_SIZE)

        numero_magico = dados[
            DESLOCAMENTO_MAGICO:DESLOCAMENTO_MAGICO + 8
        ]

        if numero_magico != NUMERO_MAGICO:
            raise ValueError("Número mágico inválido")

        versao = struct.unpack(
            "<H",
            dados[DESLOCAMENTO_VERSAO:DESLOCAMENTO_VERSAO + 2],
        )[0]

        if versao != VERSAO_FORMATO:
            raise ValueError("Versão do formato inválida")

        tamanho_pagina = struct.unpack(
            "<I",
            dados[
                DESLOCAMENTO_TAMANHO_PAGINA:
                DESLOCAMENTO_TAMANHO_PAGINA + 4
            ],
        )[0]

        if tamanho_pagina != PAGE_SIZE:
            raise ValueError("Tamanho de página incompatível")

        total_paginas = struct.unpack(
            "<I",
            dados[
                DESLOCAMENTO_TOTAL_PAGINAS:
                DESLOCAMENTO_TOTAL_PAGINAS + 4
            ],
        )[0]

        if total_paginas != tamanho_arquivo // PAGE_SIZE:
            raise ValueError("Quantidade de páginas inválida")

    def le_pagina(self, numero):
        if numero < 0:
            raise ValueError("O número da página não pode ser negativo")

        with open(self.nome_arquivo, "rb") as arquivo:
            deslocamento = numero * PAGE_SIZE
            arquivo.seek(deslocamento)
            dados = arquivo.read(PAGE_SIZE)

        if len(dados) != PAGE_SIZE:
            raise ValueError("Página inexistente ou incompleta")

        return Page(numero, dados)

    def escreve_pagina(self, numero, dados):
        if numero < 0:
            raise ValueError("O número da página não pode ser negativo")

        if len(dados) != PAGE_SIZE:
            raise ValueError("A página deve possuir exatamente 4096 bytes")

        with open(self.nome_arquivo, "r+b") as arquivo:
            deslocamento = numero * PAGE_SIZE
            arquivo.seek(deslocamento)
            arquivo.write(dados)
            arquivo.flush()

    def aloca(self):
        total_paginas = self._total_paginas()
        numero = total_paginas

        with open(self.nome_arquivo, "r+b") as arquivo:
            arquivo.seek(numero * PAGE_SIZE)
            arquivo.write(bytes(PAGE_SIZE))

            total_paginas += 1

            arquivo.seek(DESLOCAMENTO_TOTAL_PAGINAS)
            arquivo.write(struct.pack("<I", total_paginas))

            arquivo.seek(DESLOCAMENTO_PRIMEIRA_PAGINA_LIVRE)
            arquivo.write(struct.pack("<I", numero))

            arquivo.flush()

        return numero

    def insere(self, registro):
        dados_registro = registro.serializa()
        tamanho_registro = len(dados_registro)

        if tamanho_registro == 0:
            raise ValueError("O registro não pode ser vazio")

        total_paginas = self._total_paginas()

        for numero in range(1, total_paginas):
            pagina = self.le_pagina(numero)

            if pagina.quantidade_registros() < pagina.capacidade(tamanho_registro):
                slot = pagina.insere_registro(dados_registro)
                self.escreve_pagina(numero, pagina.le())
                self._atualiza_primeira_pagina_livre(tamanho_registro)
                return numero, slot

        numero = self.aloca()
        pagina = self.le_pagina(numero)
        slot = pagina.insere_registro(dados_registro)
        self.escreve_pagina(numero, pagina.le())
        self._atualiza_primeira_pagina_livre(tamanho_registro)

        return numero, slot

    def _total_paginas(self):
        with open(self.nome_arquivo, "rb") as arquivo:
            arquivo.seek(DESLOCAMENTO_TOTAL_PAGINAS)
            dados = arquivo.read(4)

        return struct.unpack("<I", dados)[0]

    def _atualiza_primeira_pagina_livre(self, tamanho_registro):
        total_paginas = self._total_paginas()
        primeira_pagina_livre = 0

        for numero in range(1, total_paginas):
            pagina = self.le_pagina(numero)

            if pagina.quantidade_registros() < pagina.capacidade(tamanho_registro):
                primeira_pagina_livre = numero
                break

        with open(self.nome_arquivo, "r+b") as arquivo:
            arquivo.seek(DESLOCAMENTO_PRIMEIRA_PAGINA_LIVRE)
            arquivo.write(struct.pack("<I", primeira_pagina_livre))
            arquivo.flush()

    def sync(self):
        with open(self.nome_arquivo, "r+b") as arquivo:
            arquivo.flush()
            os.fsync(arquivo.fileno())

    def page_count(self):
        return self._total_paginas()
