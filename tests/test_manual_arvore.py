from buffer.arvore_b_plus import ArvoreBPlus

arvore = ArvoreBPlus(ordem=3) 
# Inserindo dados (Chave, Dado/Valor) 
dados = [(10, "User10"), (20, "User20"), (5, "User5"), (30, "User30"), (25, "User25"), 
         (40, "User40"), (15, "User15"),(35, "User35"), (45, "User45"), (50, "User50"), (55, "User55") ] 

for chave, valor in dados: 
    print(f"Inserindo chave {chave}...") 
    arvore.inserir(chave, valor) 
    
 
print("\nEstrutura final da árvore (Chaves por nível):") 
arvore.imprimir_arvore() 
 

