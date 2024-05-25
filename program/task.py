#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Для своего индивидуального задания лабораторной работы 2.23
# необходимо организовать конвейер, в котором сначала в
# отдельном потоке вычисляется значение первой функции,
# после чего результаты вычисления должны передаваться второй функции,
# вычисляемой в отдельном потоке. Потоки для вычисления значений
# двух функций должны запускаться одновременно.

import math
from multiprocessing import Barrier, Manager, Process


#  Пример №22
def sum1(eps, s_dict, br, lock):
    s = 0
    n = 0
    while True:
        a = 0.5 ** (4 * n + 1)/(4 * n + 1)
        if abs(a) < eps:
            break
        else:
            s += a
            n += 1
    with lock:
        s_dict["sum1"] = s
    br.wait()


# Пример №23
def sum2(eps, s_dict, br, lock):
    s = 0
    n = 1
    while True:
        a = 0.25 ** (n+2) / (n * (n + 1)*(n + 2))
        if abs(a) < eps:
            break
        else:
            s += a
            n += 1
    with lock:
        s_dict["sum2"] = s
    br.wait()


def compair(s, y1, y2, br):
    br.wait()
    
    s1 = s["sum1"]
    s2 = s["sum2"]

    print(
        f"Сумма ряда полученная для 22 Варианта: {s1},\n"
        f"Контрольное значение y: {y1}, Разница: {abs(s1 - y1)}"
    )
    print(
        f"Сумма ряда полученная для 23 Варианта: {s2},\n"
        f"Контрольное значение y: {y2}, Разница: {abs(s2 - y2)}"
    )


def main(m):
    s = m.dict()

    br = Barrier(3)
    lock = m.Lock()

    eps = 1e-7
    # Для примера №22
    y1 = 0.5 * math.log(3) + 0.5 * math.atan(0.5)
    # Для примера №23
    y2 = -5/64 - 9/32 * math.log(0.75)

    process1 = Process(target=sum1, args=(eps, s, br, lock))
    process2 = Process(target=sum2, args=(eps, s, br, lock))
    process3 = Process(target=compair, args=(s, y1, y2, br))

    # Запуск потоков
    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()


if __name__ == "__main__":
    with Manager() as manager:
        main(manager)
    