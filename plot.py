from dataclasses import dataclass

from plant import Plant


@dataclass
class Plot:
    position: int
    plant: Plant | None = None

    @property
    def is_empty(self):
        return self.plant is None

    def to_dict(self):
        return {
            "position": self.position,
            "plant": None if self.plant is None else self.plant.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        plant_data = data.get("plant")
        return cls(
            position=int(data["position"]),
            plant=None if plant_data is None else Plant.from_dict(plant_data),
        )