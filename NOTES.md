# Módulo 1 — Armazenamento

A decisão de projeto deste módulo foi representar o armazenamento físico usando páginas de tamanho fixo de 4096 bytes e registros de tamanho fixo. A classe Page representa uma página em memória, FixedRecord transforma os valores inteiros do registro em bytes, e DataFile é responsável por persistir páginas no arquivo de dados.
Também foi incluída a página 0 como página de metadados, contendo número mágico, versão do formato, tamanho da página, total de páginas e a primeira página com espaço livre. As páginas de dados começam a partir da página 1.
Para um registro de 8 bytes inserido no slot 0 da página 1, o registro começa no byte 4112 do arquivo. A página 0 ocupa os bytes 0 a 4095, a página 1 começa no byte 4096 e seus primeiros 16 bytes são o cabeçalho. Portanto, o primeiro registro começa em 4096 + 16 = 4112.
A responsabilidade de páginas sujas e escrita controlada pelo cache fica para o Módulo 2, quando será implementado o Buffer Pool.

