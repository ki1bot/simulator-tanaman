import json
from pathlib import Path

from exceptions import SaveGameError


class SaveManager:
    def __init__(self, file_path):
        path = Path(file_path)

        if not path.is_absolute():
            path = (
                Path(__file__)
                .resolve()
                .parent
                / path
            )

        self.file_path = path

    def exists(self):
        return self.file_path.exists()

    def save(self, data):
        temp_path = (
            self.file_path.with_name(
                f"{self.file_path.name}.tmp"
            )
        )

        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with temp_path.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            temp_path.replace(
                self.file_path
            )

        except (
            OSError,
            TypeError,
            ValueError,
        ) as exc:
            raise SaveGameError(
                f"Gagal menyimpan "
                f"permainan: {exc}"
            ) from exc

    def load(self):
        if not self.exists():
            raise SaveGameError(
                "Belum ada save game."
            )

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except (
            OSError,
            json.JSONDecodeError,
        ) as exc:
            raise SaveGameError(
                f"Gagal membaca "
                f"save game: {exc}"
            ) from exc

        if not isinstance(
            data,
            dict,
        ):
            raise SaveGameError(
                "Format save game "
                "tidak valid."
            )

        return data