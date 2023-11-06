from abc import ABC, abstractmethod

from matplotlib import pyplot

from time_profiler_soa.tps_types import Numeric


class Drawer(ABC):
    def __init__(self, x_values: list[Numeric], y_values: list[Numeric]):
        self.x_values = x_values
        self.y_values = y_values

    @abstractmethod
    def draw(self) -> None:
        ...


class ImageDrawer(Drawer):
    def __init__(self, x_values: list[Numeric], y_values: list[Numeric], filepath: str):
        super().__init__(x_values, y_values)
        self.filepath = filepath

    def draw(self) -> None:
        pyplot.plot(self.x_values, self.y_values)
        pyplot.savefig(self.filepath)
