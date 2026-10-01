from collections import OrderedDict


class Cache:
    def __init__(self, pager, capacidade=16):
        self.pager = pager              #datafile
        self.capacidade = capacidade    #quantas páginas que podem ficar na memória

        self.frames = {}            #páginas atualmente armazenadas no cache
        self.suja = set()           #páginas que foram modificadas na memória e não foram gravadas no disco
        self.fixada = {}            #quantidade de vezes que a página esta sendo utilizada 
        self.uso = OrderedDict()    #ordem das paginas que foram acessadas

        self.acertos = 0    #quantidade de vezes que a página foi encontrada no cache
        self.faltas = 0     #quantidade de vezes que a página não foi encontrada no cache
    
    #reserva uma página para usar
    def fixa(self, numero): 
        if numero in self.frames:   #verifica se a página está no cache
            self.acertos += 1
            self.uso.move_to_end(numero) #verifica qual foi a última página acessada
        else:
            self.faltas += 1

            if len(self.frames) == self.capacidade: #verifica se o cache está cheio
                self._expulsa()

            self.frames[numero] = self.pager.le_pagina(numero)
            self.uso[numero] = True

        self.fixada[numero] = self.fixada.get(numero, 0) + 1

        return self.frames[numero]
    
    #liberar uma página que estava sendo usada pelo cache.
    def solta(self, numero, sujou=False):   
        if numero not in self.frames:   #verifica se a página está no cache
            raise ValueError("A página não está no cache")

        if self.fixada.get(numero, 0) <= 0: #verifica se a página está fixada
            raise ValueError("A página não está fixada")

        if sujou:   #verifica se a página foi modificada
            self.suja.add(numero)

        self.fixada[numero] -= 1
        
    #expulsa uma página do cache, caso ela não esteja fixada e se estiver suja, grava no disco.
    def _expulsa(self):
        for numero in self.uso:
            if self.fixada.get(numero, 0) == 0: #verifica se a página não está fixada
                if numero in self.suja:   #verifica se a página foi modificada
                    self.pager.escreve_pagina(numero, self.frames[numero].le())
                    self.suja.remove(numero)

                del self.frames[numero]
                del self.uso[numero]
                return

        raise RuntimeError("Todas as páginas estão fixadas para expulsar")
    
    #grava todas as páginas sujas no disco
    def descarrega(self):
        for numero in list(self.suja):
            self.pager.escreve_pagina(numero, self.frames[numero].le())
        
        self.suja.clear()   #limpa a lista de páginas sujas
        self.pager.sync()   #garante a sincronização com o arquivo