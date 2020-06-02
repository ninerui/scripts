# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def func(st):
    for i in range(1, int(len(st) / 2) + 1):
        for j in range(len(st)):
            if st[j: j + 1] == st[j + 1:j + 2 * i]:
                k = j + 1
                while st[k:k + 1] == st[k + i: k + 2 * i] and k < len(st):
                    k = k + i
                st = st[:j] + st[k:]
    return st


if __name__ == '__main__':
    st = '你好,iu就安慰返回哇哈你好哈的撒互动哈哈哈哈哈阿斯顿i七五功夫i阿飞你去废弃物哟阿斯顿发布微博覅阿斯蒂芬阿斯蒂芬我覅哦啊回复阿斯蒂芬'
    res = func(st)
    print(res)
