import struct
from storage.page import PAGE_SIZE, Page

class No:
    def __init__(self, eh_folha=True):
        self.eh_folha = eh_folha
        self.chaves = []
        self.valores = []
        self.filhos = []
        self.proximo = None


"""Versão da árvore B+ preparada para armazenar nós em páginas."""
class ArvoreBPlusIndice:

    TIPO_FOLHA = 0
    TIPO_INTERNO = 1
    SEM_PROXIMA = 0
    PAGINA_METADADOS = 1
    SEM_RAIZ = 0
    MARCA_INDICE = b"BPT1"
    
    def __init__(self, cache, ordem=3):
        self.cache = cache
        self.ordem = ordem
        self.raiz = None

    def serializar_no(self, no):
        dados = bytearray(PAGE_SIZE)

        tipo = self.TIPO_FOLHA if no.eh_folha else self.TIPO_INTERNO
        quantidade = len(no.chaves)

        struct.pack_into("<BH", dados, 0, tipo, quantidade)

        posicao = 3

        for chave in no.chaves:
            struct.pack_into("<q", dados, posicao, chave)
            posicao += 8

        if no.eh_folha:
            proximo = (
                self.SEM_PROXIMA
                if no.proximo is None
                else no.proximo
            )

            struct.pack_into("<I", dados, posicao, proximo)
            posicao += 4

            for valor in no.valores:
                pagina, slot = valor
                struct.pack_into("<II", dados, posicao, pagina, slot)
                posicao += 8

        else:
            for filho in no.filhos:
                struct.pack_into("<I", dados, posicao, filho)
                posicao += 4

        if posicao > PAGE_SIZE:
            raise ValueError("O nó não cabe na página.")

        return bytes(dados)

    def desserializar_no(self, dados):
        if len(dados) != PAGE_SIZE:
            raise ValueError("A página tem tamanho inválido.")

        tipo, quantidade = struct.unpack_from("<BH", dados, 0)

        if tipo not in (self.TIPO_FOLHA, self.TIPO_INTERNO):
            raise ValueError("Tipo de nó inválido.")

        no = No(eh_folha=(tipo == self.TIPO_FOLHA))
        posicao = 3

        for _ in range(quantidade):
            chave = struct.unpack_from("<q", dados, posicao)[0]
            no.chaves.append(chave)
            posicao += 8

        if no.eh_folha:
            proximo = struct.unpack_from("<I", dados, posicao)[0]
            posicao += 4

            no.proximo = None if proximo == self.SEM_PROXIMA else proximo

            for _ in range(quantidade):
                pagina, slot = struct.unpack_from("<II", dados, posicao)
                no.valores.append((pagina, slot))
                posicao += 8

        else:
            for _ in range(quantidade + 1):
                filho = struct.unpack_from("<I", dados, posicao)[0]
                no.filhos.append(filho)
                posicao += 4

        return no
    
    def salvar_no(self, numero_pagina, no):
        pagina = self.cache.fixa(numero_pagina)

        try:
            dados = self.serializar_no(no)
            pagina.escreve(dados)
            self.cache.solta(numero_pagina, sujou=True)
        except Exception:
            if self.cache.fixada.get(numero_pagina, 0) > 0:
                self.cache.solta(numero_pagina)
            raise

    def carregar_no(self, numero_pagina):
        pagina = self.cache.fixa(numero_pagina)

        try:
            dados = pagina.le()
            return self.desserializar_no(dados)
        finally:
            self.cache.solta(numero_pagina)
    
    """Cria a página de metadados e a primeira raiz."""
    def inicializar_indice(self):
        arquivo = self.cache.pager
        pagina_metadados = arquivo.aloca()
        if pagina_metadados != self.PAGINA_METADADOS:
            raise RuntimeError("Número inesperado para a página de metadados.")

        numero_raiz = arquivo.aloca()
        raiz = No(eh_folha=True)
        self.salvar_no(numero_raiz, raiz)
        self.raiz = numero_raiz
        self.salvar_metadados(numero_raiz)
        self.cache.descarrega()

    """Grava a identificação do índice e o número da raiz."""
    def salvar_metadados(self, numero_raiz):
        import struct
        pagina = self.cache.fixa(self.PAGINA_METADADOS)

        try:
            dados = bytearray(PAGE_SIZE)
            dados[:4] = self.MARCA_INDICE
            struct.pack_into("<I", dados, 4, numero_raiz)
            pagina.escreve(bytes(dados))
            self.cache.solta(self.PAGINA_METADADOS, sujou=True)
        except Exception:
            if self.cache.fixada.get(self.PAGINA_METADADOS, 0) > 0:
                self.cache.solta(self.PAGINA_METADADOS)
            raise
    
    """Recupera o número da raiz a partir do arquivo de índice."""
    def carregar_metadados(self):
        import struct
        pagina = self.cache.fixa(self.PAGINA_METADADOS)

        try:
            dados = pagina.le()
            if dados[:4] != self.MARCA_INDICE:
                raise ValueError("Arquivo não contém metadados de índice B+.")
            self.raiz = struct.unpack_from("<I", dados, 4)[0]

            if self.raiz == self.SEM_RAIZ:
                raise ValueError("O índice não possui raiz cadastrada.")
            return self.raiz
        finally:
            self.cache.solta(self.PAGINA_METADADOS)

    
    def buscar(self, chave):
        if self.raiz is None:
            return None

        numero_pagina = self.raiz

        while True:
            no = self.carregar_no(numero_pagina)

            # Se for um nó interno, escolhe o caminho da busca.
            if not no.eh_folha:
                indice = 0

                while (
                    indice < len(no.chaves)
                    and chave >= no.chaves[indice]
                ):
                    indice += 1

                numero_pagina = no.filhos[indice]

            else:
                # Se for uma folha, procura a chave.
                for indice, chave_atual in enumerate(no.chaves):
                    if chave_atual == chave:
                        return no.valores[indice]

                    if chave_atual > chave:
                        return None

                return None

    def encontrar_folha(self, chave):
        if self.raiz is None:
            return None

        numero_pagina = self.raiz

        while True:
            no = self.carregar_no(numero_pagina)

            if no.eh_folha:
                return numero_pagina, no

            indice = 0
            while (
                indice < len(no.chaves)
                and chave >= no.chaves[indice]
            ):
                indice += 1

            numero_pagina = no.filhos[indice]
            
    
    def inserir(self, chave, valor):
        if self.raiz is None:
            raise RuntimeError("A árvore não foi inicializada.")

        numero_pagina, folha = self.encontrar_folha(chave)
        # verifica se a chave já existe na folha
        if chave in folha.chaves:
            raise ValueError("Chave já existe na árvore.")
        
        indice = 0
        
        # insere a chave e o valor na folha.
        while indice < len(folha.chaves) and chave > folha.chaves[indice]:
            indice += 1

        folha.chaves.insert(indice, chave)
        folha.valores.insert(indice, valor)

        # Se a folha estourou, divide-a.
        if len(folha.chaves) >= self.ordem:
            self._dividir_folha(numero_pagina, folha)
        else:
            self.salvar_no(numero_pagina, folha)
        
    def _encontrar_pai(self, numero_filho):
        if self.raiz is None or numero_filho == self.raiz:
            return None
        pendentes = [self.raiz]

        while pendentes:
            # Busca em largura para encontrar o pai do nó filho.
            numero_pagina = pendentes.pop()
            no = self.carregar_no(numero_pagina)
            
            # Se o nó é uma folha, ele não pode ser pai de outro nó.
            if no.eh_folha:
                continue
            
            # Se o nó contém o número do filho, então ele é o pai.
            if numero_filho in no.filhos:
                return numero_pagina, no
            pendentes.extend(no.filhos)
            
        raise ValueError("Nó filho não encontrado na árvore.")
    
    def _inserir_no_pai(self, numero_esquerdo, chave, numero_direito):
        
        #Se a folha dividida era a raiz antiga, cria uma nova raiz
        if numero_esquerdo == self.raiz:
            nova_raiz = No(eh_folha=False)
            nova_raiz.chaves = [chave]
            nova_raiz.filhos = [numero_esquerdo, numero_direito]
            numero_nova_raiz = self.cache.pager.aloca()
            self.salvar_no(numero_nova_raiz, nova_raiz)
            self.raiz = numero_nova_raiz
            self.salvar_metadados(numero_nova_raiz)
            return

        resultado = self._encontrar_pai(numero_esquerdo)
        if resultado is None:
            raise ValueError("Nao foi possivel encontrar o nó pai")
        
        numero_pai,no_pai = resultado
        indice_filho = no_pai.filhos.index(numero_esquerdo)
        
        indice = 0
        while indice < len(no_pai.chaves) and no_pai.chaves[indice] < chave:
            indice += 1

        no_pai.chaves.insert(indice, chave)
        no_pai.filhos.insert(indice + 1, numero_direito)

        if len(no_pai.chaves) >= self.ordem:
            self._dividir_interno(numero_pai, no_pai)
        else:
            self.salvar_no(numero_pai, no_pai)
        

    def _dividir_folha(self, numero_pagina, folha):
    # Divide as chaves e os RIDs em duas folhas.
        meio = len(folha.chaves) // 2
        
        nova_folha = No(eh_folha=True)
        nova_folha.chaves = folha.chaves[meio:]
        nova_folha.valores = folha.valores[meio:]
        folha.chaves = folha.chaves[:meio]
        folha.valores = folha.valores[:meio]
    
        # Cria a nova folha em uma página do arquivo.
        numero_nova_pagina = self.cache.pager.aloca()
    
        # Mantém o encadeamento entre as folhas.
        nova_folha.proximo = folha.proximo
        folha.proximo = numero_nova_pagina
        self.salvar_no(numero_pagina, folha)
        self.salvar_no(numero_nova_pagina, nova_folha)
    
        # Insere a chave separadora no nó pai
        chave_separadora = nova_folha.chaves[0]
        self._inserir_no_pai(numero_pagina, chave_separadora, numero_nova_pagina)        
        
    def _dividir_interno(self, numero_pagina, no):
        meio = len(no.chaves) // 2

        # A chave do meio será promovida para o pai
        chave_promovida = no.chaves[meio]
        
        # Cria um novo nó interno para a direita
        novo_no = No(eh_folha=False)
        novo_no.chaves = no.chaves[meio + 1:]
        novo_no.filhos = no.filhos[meio + 1:]

        # Ajusta o nó interno original para conter apenas a metade esquerda
        no.chaves = no.chaves[:meio]
        no.filhos = no.filhos[:meio + 1]

        numero_novo_no = self.cache.pager.aloca()
        
        # Salva os dois nós no arquivo
        self.salvar_no(numero_pagina, no)
        self.salvar_no(numero_novo_no, novo_no)

        self._inserir_no_pai(numero_pagina,chave_promovida,numero_novo_no)
