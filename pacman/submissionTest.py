#!/usr/bin/python2

import collections

import submission
import util
import random

def test2a():
    lst = [0, 1, 2, 3, 4, 5]
    random.shuffle(lst)
    for item in lst:
        print(item)

if __name__ == '__main__':
    test2a()
