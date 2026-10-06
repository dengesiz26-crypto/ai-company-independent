from __future__ import annotations

from pathlib import Path
from typing import Any
import json


class JsonStore:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.base_dir / f"{name}.json"

    def load(self, name: str, default: Any = None) -> Any:
        path = self._path(name)
        if not path.exists():
            if default is None:
                return []
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default if default is not None else []

    def save(self, name: str, payload: Any) -> Any:
        path = self._path(name)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return payload

    def append(self, name: str, item: dict) -> dict:
        data = self.load(name, [])
        data.append(item)
        self.save(name, data)
        return item
