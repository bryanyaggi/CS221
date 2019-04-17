#!/usr/bin/python

import random
import collections
import math
import sys
from util import *

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    words = x.split()
    counter = collections.Counter(words)
    return dict(counter)
    # END_YOUR_CODE

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numEpochs, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each epoch.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
    epoch = 0
    while epoch < numEpochs:
        for trainExample in trainExamples:
            features = featureExtractor(trainExample[0])
            gradient = {}
            if dotProduct(weights, features) * trainExample[1] < 1:
                for feature in features:
                    gradient[feature] = -1 * features[feature] * trainExample[1]
            increment(weights, -eta, gradient)
        epoch += 1
        trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        testError = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        print("Train error = %s, Test error = %s" %(trainError, testError))
    # END_YOUR_CODE
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        minFeatureValue = 0
        maxFeatureValue = 5
        phi = {}
        for feature in weights:
            phi[feature] = random.randint(minFeatureValue, maxFeatureValue)
        y = -1
        if dotProduct(weights, phi) >= 0:
            y = 1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        chars = "".join(x.split())
        startIndex = 0
        endIndex = n - 1
        ngrams = []
        while endIndex < len(chars):
            ngrams.append(chars[startIndex : endIndex + 1])
            startIndex += 1
            endIndex += 1
        counter = collections.Counter(ngrams)
        return dict(counter)
        # END_YOUR_CODE
    return extract

############################################################
# Problem 4: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 32 lines of code, but don't worry if you deviate from this)
    
    def squaredEuclideanDistance(d1, d2):
        allKeys = list(set(d1.keys()) | set(d2.keys()))
        result = 0
        for key in allKeys:
            result += abs(d1[key] - d2[key])**2
        return result

    # Select K means randomly from examples
    random.seed(42)    
    means = []
    meanSqMag = [] # pre-calculate mean squared magnitudes
    for i in range(K):
        mean = examples[random.randint(0, K - 1)]
        means.append(mean)
        meanSqMag.append(dotProduct(mean, mean))
    assignments = [-1] * len(examples)

    # Pre-calculate example squared magnitudes
    exampleSqMags = []
    for example in examples:
        exampleSqMags.append(dotProduct(example, example))
    
    iters = 0
    quit = False
    while iters < maxIters and not(quit):

        # Step 1: for each example, assign example to cluster with closest mean
        change = False
        assignments = [-1] * len(examples)
        for i in range(len(examples)):
            minSquaredDistance = -1
            for j in range(len(means)):
                squaredDistance = exampleSqMags[i] - 2 * dotProduct(examples[i], means[j]) + meanSqMag[j]
                if (assignments[i] == -1) or (squaredDistance < minSquaredDistance):
                    minSquaredDistance = squaredDistance
                    if assignments[i] != j:
                        change = True
                    assignments[i] = j
        if not(change):
            quit = True
            continue

        # Step 2: for each cluster, set mean to that of examples in cluster
        change = False
        for i in range(len(means)):
            mean = collections.defaultdict(float)
            numExamples = 0.0
            for j in range(len(examples)):
                if assignments[j] == i:
                    increment(mean, 1, examples[j])
                    numExamples += 1
            for key in mean:
                mean[key] = mean[key] / numExamples
            if means[i] != mean:
                change = True
            means[i] = mean
            meanSqMag[i] = dotProduct(mean, mean) # pre-calculate mean squared magnitudes
        if not(change):
            quit = True
        iters += 1

    # Calculate final loss
    loss = 0
    for i in range(len(examples)):
        loss += squaredEuclideanDistance(means[assignments[i]], examples[i])
    print("iterations = %s" %iters)

    return (means, assignments, loss)
    # END_YOUR_CODE
