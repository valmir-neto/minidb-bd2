# Módulo 1 — Armazenamento

A primeira decisão de projeto foi representar o armazenamento em páginas de tamanho fixo de 4096 bytes. A classe `Page` mantém uma página em memória e registra quando ela foi modificada, enquanto `DataFile` é responsável por ler e escrever páginas diretamente no arquivo de dados. Essa separação prepara o MiniDB para receber o Buffer Pool no próximo módulo.
