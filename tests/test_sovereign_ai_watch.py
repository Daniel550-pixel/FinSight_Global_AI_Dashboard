"""import hashlib
import json
from datetime import datetime
from pathlib import Path

import pytest

import sovereign_ai_watch as saw


def test_file_hash(tmp_path):
    p = tmp_path / "f.py"
    p.write_text("print('hello world')", encoding="utf-8")
    expected = hashlib.sha256(p.read_bytes()).hexdigest()
    assert saw.file_hash(p) == expected


def test_atomic_write_and_read(tmp_path):
    path = tmp_path / "out.json"
    data = {"a": 1, "b": "x"}
    saw.atomic_write(path, data)
    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8")) == data


def test_utc_now_iso_parseable():
    ts = saw.utc_now_iso()
    # Should be parseable by datetime.fromisoformat
    _ = datetime.fromisoformat(ts)


def test_collect_priority_files(tmp_path, monkeypatch):
    # Create a minimal features tree and an expected map
    base = tmp_path / "features"
    (base / "sectors" / "finance").mkdir(parents=True)
    target = base / "sectors" / "finance" / "analysis.py"
    target.write_text("print('analysis')", encoding="utf-8")

    # Patch module globals so the function operates on our temp tree
    monkeypatch.setattr(saw, "BASE_DIR", base)
    monkeypatch.setattr(
        saw,
        "EXPECTED",
        {
            "sectors": {
                "finance": {"file": "analysis.py", "priority": 1},
            }
        },
    )

    # Clear tracking state so detection is deterministic
    saw.deployed.clear()
    saw.activity.clear()

    priority_files = saw.collect_priority_files()
    assert 1 in priority_files
    assert target in priority_files[1]

    key = str(target)
    assert key in saw.activity
    assert saw.activity[key]["updates"] == 1


if __name__ == "__main__":
    pytest.main(["-q"])"""