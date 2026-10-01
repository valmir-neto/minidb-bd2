import unittest

from storage.record import FixedRecord


class TestRegistroFixo(unittest.TestCase):
    def test_serializacao_e_desserializacao(self):
        original = FixedRecord((1, 20260001))

        dados = original.serializa()
        restaurado = FixedRecord.desserializa(dados)

        self.assertEqual(len(dados), 8)
        self.assertEqual(restaurado.valores, (1, 20260001))

    def test_little_endian(self):
        registro = FixedRecord((1, 2))
        dados = registro.serializa()
        esperado = b"\x01\x00\x00\x00" b"\x02\x00\x00\x00"

        self.assertEqual(dados, esperado)


if __name__ == "__main__":
    unittest.main()
