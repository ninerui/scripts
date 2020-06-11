# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# 一次性读取
with open("big_file.txt", "r") as fp:
    content = fp.read()


# 生成器逐行返回
def read_from_file(filename):
    with open(filename, "r") as fp:
        yield fp.readline()


# 如果一行就非常大, 逐行就不可取
# 解决办法, 每次读取指定固定大小的内容, 每次读取8k的内容
def read_from_file(filename, block_size=1024 * 8):
    with open(filename, "r") as fp:
        while True:
            chunk = fp.read(block_size)
            if not chunk:
                break

            yield chunk


from functools import partial


# 偏函数和iter优化后
def read_from_file(filename, block_size=1024 * 8):
    with open(filename, "r") as fp:
        for chunk in iter(partial(fp.read, block_size), ""):
            yield chunk
