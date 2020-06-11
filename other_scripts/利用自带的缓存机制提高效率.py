# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from functools import lru_cache


# @functools.lru_cache(maxsize=None, typed=False)
# maxsize：最多可以缓存多少个此函数的调用结果，如果为None，则无限制，设置为 2 的幂时，性能最佳；
# typed：若为 True，则不同参数类型的调用将分别缓存。

@lru_cache(maxsize=None)
def add(x, y):
    print("calculating: {} + {}".format(x, y))
    return x + y


print(add(1, 2))
print(add(1, 2))
print(add(2, 3))
print(add(1, 2))


def fib(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)

import timeit
print(timeit.timeit(lambda :fib(40), number=1))
# output: 31.2725698948
@lru_cache(None)
def fib1(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)


print(timeit.timeit(lambda: fib1(500), number=1))