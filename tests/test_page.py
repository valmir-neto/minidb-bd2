import unittest

from storage.page import PAGE_SIZE, Page
from storage.record import FixedRecord


class TestPagina(unittest.TestCase):
    def test_pagina_vazia(self):
        pagina = Page(0)

        self.assertEqual(len(pagina.read()), PAGE_SIZE)
        self.assertEqual(pagina.record_count(), 0)

    def test_adicionar_e_ler_registro(self):
        pagina = Page(0)
        registro = FixedRecord((1, 20260001)).serialize()

        numero = pagina.append_record(registro)

        self.assertEqual(numero, 0)
        self.assertEqual(pagina.record_count(), 1)
        self.assertEqual(pagina.get_record(0, len(registro)), registro)

    def test_multiplos_registros_fixos(self):
        pagina = Page(0)

        registros = [
            FixedRecord((1, 20260001)).serialize(),
            FixedRecord((2, 20260002)).serialize(),
            FixedRecord((3, 20260003)).serialize(),
        ]

        for registro in registros:
            pagina.append_record(registro)

        self.assertEqual(pagina.record_count(), 3)

        for numero, esperado in enumerate(registros):
            self.assertEqual(
                pagina.get_record(numero, len(esperado)),
                esperado
            )


if __name__ == "__main__":
    unittest.main()
