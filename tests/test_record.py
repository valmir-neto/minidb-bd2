import unittest

from storage.record import FixedRecord


class TestFixedRecord(unittest.TestCase):
    def test_record_serialization(self):
        original = FixedRecord((1, 20260001))

        data = original.serialize()
        restored = FixedRecord.deserialize(data)

        self.assertEqual(len(data), 8)
        self.assertEqual(restored.values, (1, 20260001))


if __name__ == "__main__":
    unittest.main()
