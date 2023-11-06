from pprint import pprint

from time_profiler_soa.drawer import ImageDrawer
from time_profiler_soa.time_profile_solver import RequestWayMapper, TimeProfileSolver


def main():
    C_TIME = 17
    PLOT_PATH = "plot.jpg"

    tps = TimeProfileSolver(
        [
            [0.51, 0.43, 0.06],
            [0.36, 0.03, 0.61],
            [0.17, 0.83],
        ],
        [[3, 6, 9], [2, 3, 4], [9, 7]],
    )

    tps.solve_request_ways()

    print("Все ряды:")
    pprint(tps.results)

    tps.sort_last_row()
    print("Последний ряд после сортировки")
    pprint(tps.get_last_row())

    tps.collect_last_row()
    print("Последний ряд после сборки")
    pprint(tps.get_last_row())

    e = tps.get_math_expectation()
    print("Мат. ожидание")
    pprint(e)

    d = tps.get_variance()
    print("Дисперсия")
    pprint(d)

    r = tps.get_risk(C_TIME)
    print("Риск")
    pprint(r)

    ImageDrawer(*RequestWayMapper(tps.get_last_row()).map(), PLOT_PATH).draw()


if __name__ == "__main__":
    main()
