# Módulo 1 — Armazenamento

A decisão de projeto deste módulo foi representar o armazenamento físico usando páginas de tamanho fixo de 4096 bytes e registros de tamanho fixo. A classe Page representa uma página em memória, FixedRecord transforma os valores inteiros do registro em bytes, e DataFile é responsável por persistir páginas no arquivo de dados. A responsabilidade de páginas sujas e escrita controlada pelo cache fica para o Módulo 2, quando será implementado o Buffer Pool.
