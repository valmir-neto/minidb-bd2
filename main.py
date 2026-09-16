from storage.data_file import DataFile
from storage.page import Page
from storage.record import FixedRecord


def main():
    arquivo = DataFile("dados.db")
    pagina = Page(0)

    aluno1 = FixedRecord((1, 20260001))
    aluno2 = FixedRecord((2, 20260002))

    pagina.append_record(aluno1.serialize())
    pagina.append_record(aluno2.serialize())

    arquivo.write_page(pagina.page_id, pagina.read())

    pagina_lida = arquivo.read_page(0)

    for numero in range(pagina_lida.record_count()):
        dados = pagina_lida.get_record(numero, aluno1.size)
        aluno = FixedRecord.deserialize(dados)
        print("|".join(str(valor) for valor in aluno.values))

    print(f"({pagina_lida.record_count()} registros)")


if __name__ == "__main__":
    main()
