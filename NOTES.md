# Módulo 1 — Armazenamento

A decisão de projeto deste módulo foi representar o armazenamento físico usando páginas de tamanho fixo de 4096 bytes e registros de tamanho fixo. A classe Page representa uma página em memória, FixedRecord transforma os valores inteiros do registro em bytes, e DataFile é responsável por persistir páginas no arquivo de dados.
Também foi incluída a página 0 como página de metadados, contendo número mágico, versão do formato, tamanho da página, total de páginas e a primeira página com espaço livre. As páginas de dados começam a partir da página 1.
Para um registro de 8 bytes inserido no slot 0 da página 1, o registro começa no byte 4112 do arquivo. A página 0 ocupa os bytes 0 a 4095, a página 1 começa em 4096 e seus primeiros 16 bytes são o cabeçalho. Portanto, o primeiro registro começa em 4096 + 16 = 4112.
A responsabilidade de páginas sujas e escrita controlada pelo cache fica para o Módulo 2, quando será implementado o Buffer Pool.

# Módulo 2 — Cache de páginas

A decisão de projeto deste módulo foi implementar um cache de páginas (Buffer Pool) em memória para evitar acessos desnecessários ao arquivo de dados. A classe Cache mantém as páginas carregadas em frames e controla a quantidade de vezes em que cada página está sendo utilizada.
Foi utilizado o algoritmo LRU para escolher qual página será removida quando o cache estiver cheio. A página menos recentemente utilizada é escolhida para expulsão, desde que não esteja fixada.
Foi implementado também o controle de páginas sujas. Quando uma página é modificada, ela é marcada como suja e, antes de ser removida do cache, seu conteúdo é gravado novamente no arquivo de dados. O método descarrega() permite gravar todas as páginas sujas no disco.
A capacidade padrão escolhida para o cache foi de 16 páginas. Nos testes foram utilizadas capacidades menores, como 1 e 3 páginas, para forçar situações de expulsão e verificar o funcionamento do LRU.
A principal decisão do módulo foi utilizar LRU em vez de FIFO, pois a ordem de acesso às páginas precisa ser atualizada a cada acesso para identificar corretamente a página menos recentemente utilizada.
A implementação da árvore B+ e suas operações de busca e inserção serão realizadas no Módulo 3.

# Módulo 3 — Árvore B+

A classe `ArvoreBPlusIndice` implementa uma árvore B+ com nós armazenados em páginas de 4096 bytes, utilizando o cache do Módulo 2. O índice permite localizar registros por chave sem precisar percorrer toda a tabela.
Cada nó é representado em uma página. Os três primeiros bytes armazenam o tipo do nó e a quantidade de chaves, seguidos pelas chaves em inteiros de 64 bits. Nos nós folha, também são armazenados o número da página da próxima folha e os RIDs dos registros, compostos pelo número da página e pela posição do registro. Nos nós internos, são armazenadas as referências às páginas dos filhos.
A busca percorre a árvore a partir da raiz até encontrar a folha correspondente. A inserção mantém as chaves em ordem crescente e rejeita chaves duplicadas. Quando um nó ultrapassa o limite definido pela ordem da árvore, ocorre uma divisão. Nas folhas, a primeira chave da folha direita é promovida ao pai e permanece na folha; nos nós internos, a chave do meio é promovida. Se necessário, a divisão continua até a criação de uma nova raiz.
Os metadados armazenam a identificação do índice e o número da página da raiz, permitindo recuperar a árvore após reabrir o arquivo. Os testes verificam a serialização e desserialização dos nós, a busca, a inserção, as divisões em vários níveis e a persistência do índice.
No Módulo 4, será desenvolvido o analisador e catálogo, responsável por traduzir comandos SQL textuais em instruções que o motor do MiniDB consiga executar.
