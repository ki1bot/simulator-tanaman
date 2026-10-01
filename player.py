from dataclasses import dataclass, field

from constants import MAX_ENERGY, PLANT_TYPES, STARTING_SEEDS
from exceptions import InsufficientCoinsError, InsufficientSeedError, NoEnergyError


@dataclass
class Player:
    name: str
    coins: int = 40
    energy: int = MAX_ENERGY
    seeds: dict = field(default_factory=lambda: dict(STARTING_SEEDS))
    total_harvested: int = 0
    total_earned: int = 0

    def require_energy(self, amount=1):
        if self.energy < amount:
            raise NoEnergyError("Energi tidak cukup. Lanjutkan ke hari berikutnya.")

    def consume_energy(self, amount=1):
        self.require_energy(amount)
        self.energy -= amount

    def reset_energy(self):
        self.energy = MAX_ENERGY

    def seed_count(self, kind):
        return self.seeds.get(kind, 0)

    def has_seed(self, kind):
        return self.seed_count(kind) > 0

    def use_seed(self, kind):
        if kind not in PLANT_TYPES:
            raise ValueError(f"Jenis tanaman tidak dikenal: {kind}")
        if self.seed_count(kind) <= 0:
            raise InsufficientSeedError(f"Bibit {PLANT_TYPES[kind]['name']} habis.")
        self.seeds[kind] = self.seed_count(kind) - 1

    def buy_seed(self, kind, quantity=1):
        if kind not in PLANT_TYPES:
            raise ValueError(f"Jenis tanaman tidak dikenal: {kind}")

        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Jumlah pembelian harus lebih dari 0.")

        total_cost = PLANT_TYPES[kind]["seed_price"] * quantity

        if self.coins < total_cost:
            raise InsufficientCoinsError(
                f"Koin tidak cukup. Butuh {total_cost} koin."
            )

        self.coins -= total_cost
        self.seeds[kind] = self.seed_count(kind) + quantity

    def receive_harvest(self, value):
        self.coins += value
        self.total_harvested += 1
        self.total_earned += value

    def to_dict(self):
        return {
            "name": self.name,
            "coins": self.coins,
            "energy": self.energy,
            "seeds": self.seeds,
            "total_harvested": self.total_harvested,
            "total_earned": self.total_earned,
        }

    @classmethod
    def from_dict(cls, data):
        seeds = dict(STARTING_SEEDS)
        saved = data.get("seeds", {})
        if isinstance(saved, dict):
            for key, value in saved.items():
                if key in PLANT_TYPES:
                    seeds[key] = max(0, int(value))

        return cls(
            name=str(data.get("name", "Pemain")),
            coins=max(0, int(data.get("coins", 40))),
            energy=max(0, min(MAX_ENERGY, int(data.get("energy", MAX_ENERGY)))),
            seeds=seeds,
            total_harvested=max(0, int(data.get("total_harvested", 0))),
            total_earned=max(0, int(data.get("total_earned", 0))),
        )