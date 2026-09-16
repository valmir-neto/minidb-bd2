from storage.page import PAGE_SIZE, Page
from storage.record import FixedRecord


def test_empty_page():
    pagina = Page(0)

    assert len(pagina.read()) == PAGE_SIZE
    assert pagina.record_count() == 0
    assert pagina.dirty is False


def test_append_and_read_record():
    pagina = Page(0)
    registro = FixedRecord((1, 20260001)).serialize()

    numero = pagina.append_record(registro)

    assert numero == 0
    assert pagina.record_count() == 1
    assert pagina.dirty is True
    assert pagina.get_record(0, len(registro)) == registro


def test_multiple_fixed_records():
    pagina = Page(0)
    registros = [
        FixedRecord((1, 20260001)).serialize(),
        FixedRecord((2, 20260002)).serialize(),
        FixedRecord((3, 20260003)).serialize(),
    ]

    for registro in registros:
        pagina.append_record(registro)

    assert pagina.record_count() == 3

    for numero, esperado in enumerate(registros):
        assert pagina.get_record(numero, len(esperado)) == esperado


if __name__ == "__main__":
    test_empty_page()
    test_append_and_read_record()
    test_multiple_fixed_records()
    print("Testes de página: OK")
