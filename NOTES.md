# Módulo 1 — Armazenamento

A decisão de projeto deste módulo foi representar o armazenamento físico usando páginas de tamanho fixo de 4096 bytes e registros de tamanho fixo. A classe Page representa uma página em memória, FixedRecord transforma os valores inteiros do registro em bytes, e DataFile é responsável por persistir páginas no arquivo de dados.
Também foi incluída a página 0 como página de metadados, contendo número mágico, versão do formato, tamanho da página, total de páginas e a primeira página com espaço livre. As páginas de dados começam a partir da página 1.
Para um registro de 8 bytes inserido no slot 0 da página 1, o registro começa no byte 4112 do arquivo. A página 0 ocupa os bytes 0 a 4095, a página 1 começa no byte 4096 e seus primeiros 16 bytes são o cabeçalho. Portanto, o primeiro registro começa em 4096 + 16 = 4112.
A responsabilidade de páginas sujas e escrita controlada pelo cache fica para o Módulo 2, quando será implementado o Buffer Pool.

# Módulo 2 — Cache de paginas

A decisão de projeto deste módulo foi implementar um cache de páginas (Buffer Pool) em memória para evitar acessos desnecessários ao arquivo de dados. A classe Cache mantém as páginas carregadas em frames e controla a quantidade de vezes em que cada página está sendo utilizada.
Foi utilizado o algoritmo LRU para escolher qual página será removida quando o cache estiver cheio. A página menos recentemente utilizada é escolhida para expulsão, desde que não esteja fixada.
Foi implementado também o controle de páginas sujas. Quando uma página é modificada, ela é marcada como suja e, antes de ser removida do cache, seu conteúdo é gravado novamente no arquivo de dados. O método descarrega() permite gravar todas as páginas sujas no disco.
A capacidade padrão escolhida para o cache foi de 16 páginas. Nos testes foram utilizadas capacidades menores, como 1 e 3 páginas, para forçar situações de expulsão e verificar o funcionamento do LRU.
A principal decisão do módulo foi utilizar LRU em vez de FIFO, pois a ordem de acesso às páginas precisa ser atualizada a cada acesso para identificar corretamente a página menos recentemente utilizada.
A implementação da árvore B+ e suas operações de busca e inserção serão realizadas no Módulo 3.
