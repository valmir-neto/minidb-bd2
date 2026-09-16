from storage.record import FixedRecord


def test_record_serialization():
    original = FixedRecord((1, 20260001))

    data = original.serialize()
    restored = FixedRecord.deserialize(data)

    assert len(data) == 8
    assert restored.values == (1, 20260001)


if __name__ == "__main__":
    test_record_serialization()
    print("Teste de registro fixo: OK")
