from pathlib import Path

from kusteai.memory import MemoryStore


def test_memory_store_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "mem.db"
    store = MemoryStore(str(db))

    store.save_message("user", "привет")
    store.save_message("assistant", "здравствуй")
    store.save_memory("владелец любит кофе")

    assert store.get_recent_messages() == [
        ("user", "привет"),
        ("assistant", "здравствуй"),
    ]
    assert store.get_recent_memories() == ["владелец любит кофе"]
