from dataclasses import dataclass
from random import Random

from constants import PLANT_TYPES
from exceptions import GameError


@dataclass
class Plant:
    kind: str
    growth: int = 0
    health: int = 100
    watered_today: bool = False
    cared_today: bool = False

    def __post_init__(self):
        if self.kind not in PLANT_TYPES:
            raise ValueError(f"Jenis tanaman tidak dikenal: {self.kind}")

        self.growth = max(0, int(self.growth))
        self.health = max(0, min(int(self.health), self.max_health))
        self.watered_today = bool(self.watered_today)
        self.cared_today = bool(self.cared_today)

    @property
    def meta(self):
        return PLANT_TYPES[self.kind]

    @property
    def name(self):
        return self.meta["name"]

    @property
    def grow_days(self):
        return self.meta["grow_days"]

    @property
    def harvest_value(self):
        return self.meta["harvest_value"]

    @property
    def max_health(self):
        return self.meta["max_health"]

    @property
    def leaf_color(self):
        return self.meta["leaf_color"]

    @property
    def fruit_color(self):
        return self.meta["fruit_color"]

    @property
    def is_dead(self):
        return self.health <= 0

    @property
    def is_ready(self):
        return not self.is_dead and self.growth >= self.grow_days

    @property
    def stage_name(self):
        if self.is_dead:
            return "Mati"

        if self.is_ready:
            return "Siap Panen"

        ratio = self.growth / self.grow_days

        if ratio <= 0:
            return "Bibit"

        if ratio < 0.35:
            return "Tunas"

        if ratio < 0.75:
            return "Tumbuh"

        return "Hampir Matang"

    @property
    def stage_level(self):
        if self.is_dead:
            return -1

        if self.is_ready:
            return 3

        ratio = self.growth / self.grow_days

        if ratio <= 0:
            return 0

        if ratio < 0.35:
            return 1

        return 2

    def water(self):
        if self.is_dead:
            raise GameError(
                f"{self.name} sudah mati dan tidak bisa disiram."
            )

        if self.watered_today:
            raise GameError(
                f"{self.name} sudah disiram hari ini."
            )

        self.watered_today = True

    def care(self):
        if self.is_dead:
            raise GameError(
                f"{self.name} sudah mati dan tidak bisa dirawat."
            )

        if self.cared_today:
            raise GameError(
                f"{self.name} sudah dirawat hari ini."
            )

        self.cared_today = True
        self.health = min(
            self.max_health,
            self.health + 10,
        )

    def advance_day(self, rng: Random):
        events = []

        if self.is_dead:
            self.watered_today = False
            self.cared_today = False
            return events

        if self.watered_today:
            if not self.is_ready:
                self.growth += 1
                events.append(
                    f"{self.name} tumbuh satu tahap."
                )

            self.health = min(
                self.max_health,
                self.health + 2,
            )
        else:
            damage = rng.randint(10, 18)

            self.health = max(
                0,
                self.health - damage,
            )

            events.append(
                f"{self.name} kekurangan air "
                f"(-{damage} kesehatan)."
            )

        if not self.is_dead:
            pest_chance = (
                0.08
                if self.cared_today
                else 0.18
            )

            if rng.random() < pest_chance:
                damage = rng.randint(7, 16)

                self.health = max(
                    0,
                    self.health - damage,
                )

                events.append(
                    f"Hama menyerang {self.name} "
                    f"(-{damage} kesehatan)."
                )

        if (
            not self.is_dead
            and self.cared_today
            and rng.random() < 0.20
        ):
            recovery = rng.randint(3, 7)
            before = self.health

            self.health = min(
                self.max_health,
                self.health + recovery,
            )

            gained = self.health - before

            if gained > 0:
                events.append(
                    f"Perawatan memulihkan "
                    f"{gained} kesehatan "
                    f"{self.name}."
                )

        if (
            not self.is_dead
            and self.watered_today
            and self.cared_today
            and not self.is_ready
            and rng.random() < 0.15
        ):
            self.growth += 1

            events.append(
                f"{self.name} mendapat "
                f"pertumbuhan bonus."
            )

        if self.health <= 0:
            events.append(
                f"{self.name} mati."
            )
        elif self.is_ready:
            events.append(
                f"{self.name} siap dipanen."
            )

        self.watered_today = False
        self.cared_today = False

        return events

    def to_dict(self):
        return {
            "kind": self.kind,
            "growth": self.growth,
            "health": self.health,
            "watered_today": self.watered_today,
            "cared_today": self.cared_today,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError(
                "Data tanaman tidak valid."
            )

        return cls(
            kind=data["kind"],
            growth=data.get("growth", 0),
            health=data.get("health", 100),
            watered_today=data.get(
                "watered_today",
                False,
            ),
            cared_today=data.get(
                "cared_today",
                False,
            ),
        )