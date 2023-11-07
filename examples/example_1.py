from pprint import pprint

from time_profiler_soa.drawer import ImageDrawer
from time_profiler_soa.time_profile_solver import RequestWayMapper, TimeProfileSolver


def main():
    C_TIME = 17
    PLOT_PATH = "plot.jpg"

    """
    probabilities
        [0.34, 0.64, 0.02]
        [0.83, 0.14, 0.03]
        [0.56, 0.44]

    times
        [5, 4, 1]
        [9, 8, 6]
        [3, 2]
    """

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

    print("Все формулы:")
    pprint([[x.formula for x in row] for row in tps.results])

    tps.sort_last_row()
    print("Последний ряд после сортировки:")
    pprint(tps.get_last_row())

    print("Формулы последнего ряда:")
    pprint([x.formula for x in tps.get_last_row()])

    tps.collect_last_row()
    print("Последний ряд после сборки")
    pprint(tps.get_last_row())

    e, e_log = tps.get_math_expectation_logged()
    print("Мат. ожидание:")
    pprint(e)
    print("Вычисление мат. ожидания:")
    print(e_log)

    d, d_log = tps.get_variance_logged()
    print("Дисперсия:")
    pprint(d)
    print("Вычисление дисперсии:")
    print(d_log)

    r, r_log = tps.get_risk_logged(C_TIME)
    print("Риск")
    pprint(r)
    print("Вычисление риска:")
    print(r_log)

    ImageDrawer(*RequestWayMapper(tps.get_last_row()).map(), PLOT_PATH).draw()


if __name__ == "__main__":
    main()
