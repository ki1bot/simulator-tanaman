from random import Random

from constants import GRID_COLS, GRID_ROWS, PLANT_TYPES
from exceptions import (
    EmptyPlotError,
    InvalidPlotError,
    PlantNotReadyError,
    PlotOccupiedError,
)
from plant import Plant
from plot import Plot


class Garden:
    def __init__(self, plots=None):
        total = GRID_ROWS * GRID_COLS
        self.plots = plots or [Plot(position=i) for i in range(1, total + 1)]

        if len(self.plots) != total:
            raise ValueError(f"Taman harus memiliki {total} petak.")

    def get_plot(self, position):
        if not 1 <= position <= len(self.plots):
            raise InvalidPlotError(
                f"Petak harus antara 1 sampai {len(self.plots)}."
            )
        return self.plots[position - 1]

    def plant_seed(self, position, kind):
        if kind not in PLANT_TYPES:
            raise ValueError(f"Jenis tanaman tidak dikenal: {kind}")

        plot = self.get_plot(position)

        if not plot.is_empty:
            raise PlotOccupiedError(f"Petak {position} sudah terisi.")

        plot.plant = Plant(kind=kind)
        return plot.plant

    def water_plot(self, position):
        plot = self.get_plot(position)
        if plot.is_empty:
            raise EmptyPlotError(f"Petak {position} kosong.")
        plot.plant.water()
        return plot.plant

    def care_plot(self, position):
        plot = self.get_plot(position)
        if plot.is_empty:
            raise EmptyPlotError(f"Petak {position} kosong.")
        plot.plant.care()
        return plot.plant

    def harvest_plot(self, position):
        plot = self.get_plot(position)
        if plot.is_empty:
            raise EmptyPlotError(f"Petak {position} kosong.")

        plant = plot.plant

        if plant.is_dead:
            raise PlantNotReadyError(
                f"Tanaman di petak {position} sudah mati. Bersihkan dulu."
            )

        if not plant.is_ready:
            raise PlantNotReadyError(
                f"{plant.name} di petak {position} belum siap dipanen."
            )

        plot.plant = None
        return plant

    def clear_dead_plot(self, position):
        plot = self.get_plot(position)
        if plot.is_empty:
            raise EmptyPlotError(f"Petak {position} kosong.")

        if not plot.plant.is_dead:
            raise PlantNotReadyError(
                f"Tanaman di petak {position} masih hidup."
            )

        dead_name = plot.plant.name
        plot.plant = None
        return dead_name

    def advance_day(self, rng: Random):
        events = []

        for plot in self.plots:
            if plot.plant is None:
                continue

            for event in plot.plant.advance_day(rng):
                events.append(f"Petak {plot.position}: {event}")

        return events

    def to_dict(self):
        return {
            "plots": [plot.to_dict() for plot in self.plots]
        }

    @classmethod
    def from_dict(cls, data):
        plots_data = data.get("plots", [])
        plots = [Plot.from_dict(item) for item in plots_data]
        return cls(plots=plots)