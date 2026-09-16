from typing import Dict, List, Optional, Tuple

class Repository:
    def __init__(self):
        self._data: Dict[int, dict] = {}
        self._next_id = 1  

    def add(self, record: dict) -> int:
        new_id = self._next_id
        self._data[new_id] = dict(record)
        self._next_id += 1
        return new_id

    def get(self, record_id: int) -> Optional[dict]:
        return self._data.get(record_id)

    def get_all(self) -> List[Tuple[int, dict]]:
        return sorted(self._data.items())

    def update(self, record_id: int, record: dict) -> bool:
        if record_id not in self._data:
            return False
        self._data[record_id] = dict(record)
        return True

    def delete(self, record_id: int) -> bool:
        return self._data.pop(record_id, None) is not None
