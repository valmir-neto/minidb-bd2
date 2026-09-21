from storage.data_file import DataFile #arquivo de dados
from storage.page import Page #representa a pagina
from storage.record import FixedRecord #registro de tamanho fixo


def main():
    arquivo = DataFile("dados.db") #cria um objeto DataFile
    pagina = Page(0) #abre\cria a pagina de número 0

    aluno1 = FixedRecord((1, 20260001)) #armazena\cria um registro (id, matricula)
    aluno2 = FixedRecord((2, 20260002))

    pagina.append_record(aluno1.serialize()) #pega o aluno e transforma em bytes e armazena esse registro dentro da pag
    pagina.append_record(aluno2.serialize())

    arquivo.write_page(pagina.page_id, pagina.read()) #grava os dados da página no arquivo dados.db na página 0.

    pagina_lida = arquivo.read_page(0) #Ler a página 0 do arquivo dados.db

    for numero in range(pagina_lida.record_count()): #descobrir quantos registros tem
        dados = pagina_lida.get_record(numero, aluno1.size) #descobre quantos registros existem na página.
        aluno = FixedRecord.deserialize(dados) #descobre os valores fixos
        print("|".join(str(valor) for valor in aluno.values))

    print(f"({pagina_lida.record_count()} registros)")


if __name__ == "__main__":
    main()
