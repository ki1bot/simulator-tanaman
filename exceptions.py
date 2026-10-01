class GameError(Exception):
    pass


class InvalidPlotError(GameError):
    pass


class PlotOccupiedError(GameError):
    pass


class EmptyPlotError(GameError):
    pass


class InsufficientSeedError(GameError):
    pass


class PlantNotReadyError(GameError):
    pass


class InsufficientCoinsError(GameError):
    pass


class NoEnergyError(GameError):
    pass


class SaveGameError(GameError):
    pass