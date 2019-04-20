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
    for n in range(4, 13):
        featureExtractor = submission.extractCharacterFeatures(n)
        print("n = %d" %n)
        submission.learnPredictor(trainExamples, devExamples, featureExtractor, numEpochs = 20, eta = 0.01)

def test4a():
    x1 = {0:1, 1:0}
    x2 = {0:1, 1:2}
    x3 = {0:3, 1:0}
    x4 = {0:2, 1:2}
    examples = [x1, x2, x3, x4]
    submission.kmeans(examples, 2, maxIters=10)

def test4b():
    x1 = {0:0, 1:0}
    x2 = {0:0, 1:1}
    x3 = {0:0, 1:2}
    x4 = {0:0, 1:3}
    x5 = {0:0, 1:4}
    x6 = {0:0, 1:5}
    examples = [x1, x2, x3, x4, x5, x6]
    centers, assignments, totalCost = submission.kmeans(examples, 2, maxIters=10)
    print("centers = %s" %centers)
    print("assignments = %s" %assignments)
    print("totalCost = %s" %totalCost)

if __name__ == '__main__':
    #test3a()
    #test3b()
    #test3c()
    #test3e()
    test3f()
    #test4b()
