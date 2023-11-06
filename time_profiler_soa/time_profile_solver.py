from dataclasses import dataclass
from functools import reduce
from typing import Tuple

from time_profiler_soa.tps_types import Numeric


@dataclass
class RequestWay:
    name: str
    probability: Numeric
    time: Numeric


class RequestWayMapper:
    def __init__(self, values: list[RequestWay]) -> None:
        self.values = values

    def map(self) -> Tuple[list[Numeric], list[Numeric]]:
        p_values = []
        t_values = []

        for v in self.values:
            p_values.append(v.probability)
            t_values.append(v.time)

        return t_values, p_values


class TimeProfileSolver:
    def __init__(
        self,
        probabilities: list[list[Numeric]],
        times: list[list[Numeric]],
        name_literal: str = "W",
    ):
        self.probabilities = probabilities
        self.times = times
        self.name_literal = name_literal
        self.results: list[list[RequestWay]] = [[]]

        self._sorted = False
        self._collected = False

    def solve_request_ways(self):
        self._sorted = False
        self._collected = False

        # first step - just append first service info to results
        for i, (p, t) in enumerate(zip(self.probabilities[0], self.times[0])):
            rw = RequestWay(f"{self.name_literal}{i + 1}", p, t)
            self.results[0].append(rw)

        for service_id in range(1, len(self.probabilities)):
            self.results.append([])

            for service_p, service_t in zip(
                self.probabilities[service_id], self.times[service_id]
            ):
                for i, last_rw in enumerate(self.results[-2]):
                    p, t = last_rw.probability, last_rw.time

                    rw = RequestWay(
                        f"{last_rw.name}{i + 1}", service_p * p, service_t + t
                    )

                    self.results[-1].append(rw)

    def sort_last_row(self):
        if self._sorted:
            return

        self._sorted = True

        self.results[-1].sort(key=lambda x: x.time)

    def collect_last_row(self):
        if self._collected:
            return

        self._collected = True

        self.sort_last_row()

        last_row = self.results.pop()
        new_last_row: list[RequestWay] = []

        for rw in last_row:
            if new_last_row and new_last_row[-1].time == rw.time:
                new_last_row[-1].probability += rw.probability
            else:
                new_last_row.append(rw)

        self.results.append(new_last_row)

    def get_math_expectation(self) -> Numeric:
        if not self._sorted:
            self.sort_last_row()

        if not self._collected:
            self.collect_last_row()

        return reduce(lambda s, v: s + (v.time * v.probability), self.get_last_row(), 0)

    def get_variance(self) -> Numeric:
        expectation = self.get_math_expectation()

        return reduce(
            lambda s, v: s + (((v.time - expectation) ** 2) * v.probability),
            self.get_last_row(),
            0,
        )

    def get_risk(self, C_time):
        if not self._sorted:
            self.sort_last_row()

        if not self._collected:
            self.collect_last_row()

        return 1 - reduce(
            lambda s, v: s + v.probability if v.time <= C_time else s,
            self.get_last_row(),
            0,
        )

    def get_last_row(self):
        return self.results[-1]
