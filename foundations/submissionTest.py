#!/usr/bin/python2

import collections

import submission

def test3a():
    print(submission.findAlphabeticallyLastWord('ball fall tall yall'))

def test3b():
    print(submission.euclideanDistance((1,5), (4,1)))

def test3c():
    print(submission.mutateSentences('the cat and the mouse'))
    print(submission.mutateSentences('a a a a a'))

def test3d():
    print(submission.sparseVectorDotProduct(collections.defaultdict(float, {'a':5}), collections.defaultdict(float, {'b':2, 'a':3})))

def test3e():
    v1 = collections.defaultdict(float, {'a':5})
    v2 = collections.defaultdict(float, {'b':2, 'a':3})
    print(submission.incrementSparseVector(v1, 2, v2))

def test3g():
    print(submission.computeLongestPalindromeLength('animal'))

if __name__ == '__main__':
    #test3a()
    #test3b()
    #test3d()
    #test3e()
    #test3c()
    test3g()
