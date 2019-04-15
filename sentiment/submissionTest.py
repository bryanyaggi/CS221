#!/usr/bin/python2

import collections

import submission

def test3a():
    print(submission.extractWordFeatures('ball fall tall yall'))

def test3b():
    trainExamples = (("hello world", 1), ("goodnight moon", -1))
    testExamples = (("hello", 1), ("moon", -1))
    submission.learnPredictor(trainExamples, testExamples, submission.extractWordFeatures, 5, .5)

if __name__ == '__main__':
    #test3a()
    test3b()
