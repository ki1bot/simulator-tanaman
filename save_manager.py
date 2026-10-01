import json
from pathlib import Path

from exceptions import SaveGameError


class SaveManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def exists(self):
        return self.file_path.exists()

    def save(self, data):
        temp_path = self.file_path.with_suffix(".tmp")

        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

            temp_path.replace(self.file_path)
        except OSError as exc:
            raise SaveGameError(f"Gagal menyimpan permainan: {exc}") from exc

    def load(self):
        if not self.exists():
            raise SaveGameError("File save belum ada.")

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            raise SaveGameError(f"Gagal membaca save game: {exc}") from exc

        if not isinstance(data, dict):
            raise SaveGameError("Format save game tidak valid.")

        return data