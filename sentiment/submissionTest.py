#!/usr/bin/python2

import collections

import submission
import util

def test3a():
    print(submission.extractWordFeatures('ball fall tall yall'))

def test3b():
    trainExamples = (("hello world", 1), ("goodnight moon", -1))
    testExamples = (("hello", 1), ("moon", -1))
    submission.learnPredictor(trainExamples, testExamples, submission.extractWordFeatures, 5, .5)

def test3c():
    print(submission.generateDataset(10, {"ball": -.75, "yall": .5}))

def test3e():
    extractor = submission.extractCharacterFeatures(2)
    print(extractor("hello world"))

def test3f():
    trainExamples = util.readExamples('polarity.train')
    devExamples = util.readExamples('polarity.dev')
    for n in range(4, 8):
        featureExtractor = submission.extractCharacterFeatures(n)
        print("n = %d" %n)
        submission.learnPredictor(trainExamples, devExamples, featureExtractor, numEpochs = 20, eta = 0.01)

if __name__ == '__main__':
    #test3a()
    #test3b()
    #test3c()
    #test3e()
    test3f()
