from random import Random

from constants import (
    GRID_COLS,
    GRID_ROWS,
    PLANT_TYPES,
)
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
        total = (
            GRID_ROWS
            * GRID_COLS
        )

        if plots is None:
            self.plots = [
                Plot(position=i)
                for i in range(
                    1,
                    total + 1,
                )
            ]
        else:
            self.plots = plots

        if len(self.plots) != total:
            raise ValueError(
                f"Taman harus memiliki "
                f"tepat {total} petak."
            )

        positions = sorted(
            plot.position
            for plot in self.plots
        )

        if positions != list(
            range(
                1,
                total + 1,
            )
        ):
            raise ValueError(
                "Nomor petak taman "
                "tidak valid."
            )

        self.plots.sort(
            key=lambda plot: (
                plot.position
            )
        )

    def get_plot(self, position):
        position = int(position)

        if not (
            1
            <= position
            <= len(self.plots)
        ):
            raise InvalidPlotError(
                f"Nomor petak harus "
                f"antara 1 dan "
                f"{len(self.plots)}."
            )

        return self.plots[
            position - 1
        ]

    def plant_seed(
        self,
        position,
        kind,
    ):
        if kind not in PLANT_TYPES:
            raise ValueError(
                f"Jenis tanaman tidak "
                f"dikenal: {kind}"
            )

        plot = self.get_plot(
            position
        )

        if not plot.is_empty:
            raise PlotOccupiedError(
                f"Petak {position} "
                f"sudah terisi."
            )

        plot.plant = Plant(
            kind=kind
        )

        return plot.plant

    def water_plot(
        self,
        position,
    ):
        plot = self.get_plot(
            position
        )

        if plot.is_empty:
            raise EmptyPlotError(
                f"Petak {position} "
                f"masih kosong."
            )

        plot.plant.water()

        return plot.plant

    def care_plot(
        self,
        position,
    ):
        plot = self.get_plot(
            position
        )

        if plot.is_empty:
            raise EmptyPlotError(
                f"Petak {position} "
                f"masih kosong."
            )

        plot.plant.care()

        return plot.plant

    def harvest_plot(
        self,
        position,
    ):
        plot = self.get_plot(
            position
        )

        if plot.is_empty:
            raise EmptyPlotError(
                f"Petak {position} "
                f"masih kosong."
            )

        plant = plot.plant

        if plant.is_dead:
            raise PlantNotReadyError(
                f"Tanaman di petak "
                f"{position} sudah mati. "
                f"Bersihkan petak "
                f"terlebih dahulu."
            )

        if not plant.is_ready:
            raise PlantNotReadyError(
                f"{plant.name} di petak "
                f"{position} belum siap "
                f"dipanen."
            )

        plot.plant = None

        return plant

    def clear_dead_plot(
        self,
        position,
    ):
        plot = self.get_plot(
            position
        )

        if plot.is_empty:
            raise EmptyPlotError(
                f"Petak {position} "
                f"masih kosong."
            )

        if not plot.plant.is_dead:
            raise PlantNotReadyError(
                f"Tanaman di petak "
                f"{position} masih hidup."
            )

        name = plot.plant.name
        plot.plant = None

        return name

    def advance_day(
        self,
        rng: Random,
    ):
        events = []

        for plot in self.plots:
            if plot.plant is None:
                continue

            for event in (
                plot.plant.advance_day(
                    rng
                )
            ):
                events.append(
                    f"Petak "
                    f"{plot.position}: "
                    f"{event}"
                )

        return events

    def to_dict(self):
        return {
            "plots": [
                plot.to_dict()
                for plot in self.plots
            ]
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "Data taman tidak valid."
            )

        plots_data = data.get(
            "plots"
        )

        if not isinstance(
            plots_data,
            list,
        ):
            raise ValueError(
                "Daftar petak taman "
                "tidak valid."
            )

        plots = [
            Plot.from_dict(item)
            for item in plots_data
        ]

        return cls(
            plots=plots
        )