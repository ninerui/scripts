# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import atexit


@atexit.register
def clean():
    print("清理任务")


def main():
    return 1 / 0

main()
