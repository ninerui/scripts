# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib


# 延迟调用
def callback():
    print("B")


with contextlib.ExitStack() as stack:
    stack.callback(callback)
    print("A")

# 输出结果:
# A
# B
