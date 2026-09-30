import unittest

from storage.record import FixedRecord


class TestRegistroFixo(unittest.TestCase):
    def test_serializacao_do_registro(self):
        original = FixedRecord((1, 20260001))

        data = original.serialize()
        restaurado = FixedRecord.deserialize(data)

        self.assertEqual(len(data), 8)
        self.assertEqual(restaurado.values, (1, 20260001))


if __name__ == "__main__":
    unittest.main()
