from abc import ABC, abstractmethod

from matplotlib import pyplot

from time_profiler_soa.tps_types import Numeric


class Drawer(ABC):
    def __init__(
        self,
        x_values: list[Numeric],
        y_values: list[Numeric],
        x_label: str = "x",
        y_label: str = "y",
    ):
        self.x_values = x_values
        self.y_values = y_values
        self.x_label = x_label
        self.y_label = y_label

    @abstractmethod
    def draw(self) -> None:
        ...


class ImageDrawer(Drawer):
    def __init__(
        self,
        x_values: list[Numeric],
        y_values: list[Numeric],
        x_label: str,
        y_label: str,
        filepath: str,
    ):
        super().__init__(x_values, y_values, x_label, y_label)
        self.filepath = filepath

    def draw(self) -> None:
        pyplot.plot(self.x_values, self.y_values)
        pyplot.xlabel(self.x_label)
        pyplot.ylabel(self.y_label)
        pyplot.savefig(self.filepath)
