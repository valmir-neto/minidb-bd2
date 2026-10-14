import math

class No:
    def __init__(self, eh_folha=False):
        self.eh_folha = eh_folha
        self.chaves = []
        self.valores = []       # Apenas para nós folha (dados ou referências)
        self.filhos = []        # Apenas para nós internos (ponteiros para outros nós)
        self.proximo = None     # Apenas para nós folha (lista encadeada)

class ArvoreBPlus:
    def __init__(self, ordem=3):
        self.raiz = No(eh_folha=True)
        self.ordem = ordem  # Número máximo de ponteiros de filhos em um nó interno

    """Buscar uma chave na árvore e retorna seu valor associado"""
    def buscar(self, chave):
        atual = self.raiz
        while not atual.eh_folha:
            atual = self._obter_no_filho(atual, chave)
            
        for posicao, chave_atual in enumerate(atual.chaves):
            if chave_atual == chave:
                return atual.valores[posicao]
        return None

    """Encontrar o nó filho correto para descer na busca/inserção"""
    def _obter_no_filho(self, no, chave):
        for posicao, chave_atual in enumerate(no.chaves):
            if chave < chave_atual:
                return no.filhos[posicao]
        return no.filhos[-1]
    
    """Insere um par chave-valor"""
    def inserir(self, chave, valor):
        raiz_atual = self.raiz
        
        # 1. Encontra a folha correta para inserção
        atual = raiz_atual
        while not atual.eh_folha:
            atual = self._obter_no_filho(atual, chave)

        # 2. Insere a chave de forma ordenada na folha
        if chave in atual.chaves:
            indice = atual.chaves.index(chave)
            atual.valores[indice] = valor  # Atualiza o valor se a chave já existir
            return
        indice = 0
        while indice < len(atual.chaves) and atual.chaves[indice] < chave:
            indice += 1
        atual.chaves.insert(indice, chave)
        atual.valores.insert(indice, valor)

        # 3. Trata o estouro (overflow) se a folha exceder o limite
        if len(atual.chaves) >= self.ordem:
            self._dividir_folha(atual)

    """Dividir um nó folha que estourou"""
    def _dividir_folha(self, folha):
        meio = math.ceil(self.ordem / 2) #math.ceil arredonda para cima o resultado
        folha_esquerda = folha
        folha_direita = No(eh_folha=True)
        
        # Conecta a lista encadeada das folhas (busca sequencial)
        folha_direita.proximo = folha_esquerda.proximo
        folha_esquerda.proximo = folha_direita
        
        # Divide as chaves e valores ao meio
        folha_direita.chaves = folha_esquerda.chaves[meio:]
        folha_direita.valores = folha_esquerda.valores[meio:]
        
        folha_esquerda.chaves = folha_esquerda.chaves[:meio]
        folha_esquerda.valores = folha_esquerda.valores[:meio]
        
        # A primeira chave da nova folha da direita sobe para o pai (promovida)
        chave_pai = folha_direita.chaves[0]
        self._inserir_no_pai(folha_esquerda, chave_pai, folha_direita)

        """Inserir uma chave promotora no nó pai e ajustar os ponteiros"""
    def _inserir_no_pai(self, esquerda, chave, direita):
        # Se o nó dividido era a raiz antiga, cria uma nova raiz
        if esquerda == self.raiz:
            nova_raiz = No(eh_folha=False)
            nova_raiz.chaves = [chave]
            nova_raiz.filhos = [esquerda, direita]
            self.raiz = nova_raiz
            return
        pai = self._encontrar_pai(self.raiz, esquerda)
        
        # Insere a chave e o novo filho de forma ordenada no pai
        indice = 0
        while indice < len(pai.chaves) and pai.chaves[indice] < chave:
            indice += 1
        pai.chaves.insert(indice, chave)
        pai.filhos.insert(indice + 1, direita)

        # Trata o estouro se o nó interno exceder o limite de chaves
        if len(pai.chaves) >= self.ordem:
            self._dividir_interno(pai)
            
    """Dividir um nó interno que estourou"""
    def _dividir_interno(self, no_interno):
        meio = math.floor(self.ordem / 2)
        no_esquerdo = no_interno
        no_direito = No(eh_folha=False)
        
        # Na divisão interna, a chave do meio SOBE e NÃO fica no nó da direita
        chave_pai = no_esquerdo.chaves[meio]
        no_direito.chaves = no_esquerdo.chaves[meio + 1:]
        no_direito.filhos = no_esquerdo.filhos[meio + 1:]
        no_esquerdo.chaves = no_esquerdo.chaves[:meio]
        no_esquerdo.filhos = no_esquerdo.filhos[:meio + 1]
    
        self._inserir_no_pai(no_esquerdo, chave_pai, no_direito)

    """Busca recursiva para encontrar o nó pai de um determinado filho"""
    def _encontrar_pai(self, atual, filho_alvo):
        if atual.eh_folha or not atual.filhos:
            return None
        for filho in atual.filhos:
            if filho == filho_alvo:
                return atual
            pai = self._encontrar_pai(filho, filho_alvo)
            if pai:
                return pai
        return None

    """Imprimir a estrutura da árvore por níveis """
    def imprimir_arvore(self):
        fila = [self.raiz]
        while fila:
            tamanho_nivel = len(fila)
            linha_nivel = ""
            for _ in range(tamanho_nivel):
                atual = fila.pop(0)
                linha_nivel += f" {str(atual.chaves)} "
                if not atual.eh_folha:
                    fila.extend(atual.filhos)
            print(linha_nivel)
            print("-" * len(linha_nivel))