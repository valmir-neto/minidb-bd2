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

A classe ArvoreBPlus organiza pares de chave e valor em uma árvore balanceada. Os nós internos guardam chaves separadoras e referências para os filhos; as folhas guardam as chaves e os valores associados. As folhas também mantêm uma referência para a próxima folha, formando uma lista encadeada.
A busca começa na raiz e percorre os nós internos até chegar à folha apropriada. A inserção mantém as chaves da folha em ordem crescente. Se uma chave já existir, o valor associado é atualizado.
A ordem padrão escolhida no código é 3. Nesta implementação, o nó é dividido quando atinge 3 chaves; por isso, uma folha mantém até 2 chaves antes de ocorrer a divisão. Na divisão de folha, a primeira chave da folha direita é promovida ao pai e permanece também na folha direita. Na divisão de nó interno, a chave do meio é promovida e removida dos nós internos resultantes. Se necessário, a divisão pode continuar até criar uma nova raiz.
Os testes do M3 verificam inserção e busca de várias chaves, divisão da raiz, divisões em níveis internos, encadeamento ordenado das folhas e atualização do valor de uma chave existente.
A árvore implementada neste módulo ainda representa o índice em memória; persistência do índice e integração com o armazenamento/cache precisam ser avaliadas conforme os requisitos da disciplina antes de considerar o módulo finalizado.
