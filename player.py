from dataclasses import dataclass, field

from constants import (
    MAX_ENERGY,
    PLANT_TYPES,
    STARTING_SEEDS,
)
from exceptions import (
    InsufficientCoinsError,
    InsufficientSeedError,
    NoEnergyError,
)


@dataclass
class Player:
    name: str
    coins: int = 40
    energy: int = MAX_ENERGY
    seeds: dict[str, int] = field(
        default_factory=lambda: dict(
            STARTING_SEEDS
        )
    )
    total_harvested: int = 0
    total_earned: int = 0

    def require_energy(self, amount=1):
        if self.energy < amount:
            raise NoEnergyError(
                "Energi tidak cukup. "
                "Lanjutkan ke hari berikutnya."
            )

    def consume_energy(self, amount=1):
        self.require_energy(amount)
        self.energy -= amount

    def reset_energy(self):
        self.energy = MAX_ENERGY

    def seed_count(self, kind):
        return self.seeds.get(kind, 0)

    def use_seed(self, kind):
        if kind not in PLANT_TYPES:
            raise ValueError(
                f"Jenis tanaman tidak dikenal: "
                f"{kind}"
            )

        if self.seed_count(kind) <= 0:
            raise InsufficientSeedError(
                f"Bibit "
                f"{PLANT_TYPES[kind]['name']} "
                f"habis."
            )

        self.seeds[kind] = (
            self.seed_count(kind) - 1
        )

    def buy_seed(
        self,
        kind,
        quantity=1,
    ):
        if kind not in PLANT_TYPES:
            raise ValueError(
                f"Jenis tanaman tidak dikenal: "
                f"{kind}"
            )

        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError(
                "Jumlah pembelian harus "
                "lebih dari 0."
            )

        total_cost = (
            PLANT_TYPES[kind]["seed_price"]
            * quantity
        )

        if self.coins < total_cost:
            raise InsufficientCoinsError(
                f"Koin tidak cukup. "
                f"Dibutuhkan "
                f"{total_cost} koin."
            )

        self.coins -= total_cost

        self.seeds[kind] = (
            self.seed_count(kind)
            + quantity
        )

    def receive_harvest(self, value):
        value = max(
            0,
            int(value),
        )

        self.coins += value
        self.total_harvested += 1
        self.total_earned += value

    def to_dict(self):
        return {
            "name": self.name,
            "coins": self.coins,
            "energy": self.energy,
            "seeds": self.seeds,
            "total_harvested": (
                self.total_harvested
            ),
            "total_earned": (
                self.total_earned
            ),
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError(
                "Data pemain tidak valid."
            )

        seeds = dict(
            STARTING_SEEDS
        )

        saved_seeds = data.get(
            "seeds",
            {},
        )

        if not isinstance(
            saved_seeds,
            dict,
        ):
            raise ValueError(
                "Data inventaris bibit "
                "tidak valid."
            )

        for key, value in (
            saved_seeds.items()
        ):
            if key in PLANT_TYPES:
                seeds[key] = max(
                    0,
                    int(value),
                )

        name = str(
            data.get(
                "name",
                "Pemain",
            )
        ).strip()

        if not name:
            name = "Pemain"

        return cls(
            name=name,
            coins=max(
                0,
                int(
                    data.get(
                        "coins",
                        40,
                    )
                ),
            ),
            energy=max(
                0,
                min(
                    MAX_ENERGY,
                    int(
                        data.get(
                            "energy",
                            MAX_ENERGY,
                        )
                    ),
                ),
            ),
            seeds=seeds,
            total_harvested=max(
                0,
                int(
                    data.get(
                        "total_harvested",
                        0,
                    )
                ),
            ),
            total_earned=max(
                0,
                int(
                    data.get(
                        "total_earned",
                        0,
                    )
                ),
            ),
        )