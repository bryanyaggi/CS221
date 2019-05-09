#!/usr/bin/python2

import collections

import submission
import util

class ValueIterationIters(util.MDPAlgorithm):
    '''
    Solve the MDP using value iteration.  Your solve() method must set
    - self.V to the dictionary mapping states to optimal values
    - self.pi to the dictionary mapping states to an optimal action
    The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
    '''
    def solve(self, mdp, numIters):
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                if state == -2 or state == 2: # prevent error if actions is empty without altering util.py
                    pi[state] = ''
                else:
                    pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi

        V = collections.defaultdict(float)  # state -> value of state
        iters = 0
        while True:
            newV = {}
            for state in mdp.states:
                # This evaluates to zero for end states, which have no available actions (by definition)
                if state == -2 or state == 2: # prevent error if actions is empty without altering util.py
                    newV[state] = 0
                else:
                    newV[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state))
            if iters >= numIters:
                break
            iters += 1
            V = newV

        # Compute the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        print "ValueIteration: %d iterations" % numIters
        self.pi = pi
        self.V = V

class BasicGameMDP(util.MDP):
    # Return a value of any type capturing the start state of the MDP.
    def startState(self):
        return 0

    def isEnd(self, state):
        if state == -2 or state == 2:
            return True
        else:
            return False

    # Return a list of strings representing actions possible from |state|.
    def actions(self, state):
        result = []
        if not(self.isEnd(state)):
            result.append('-1')
            result.append('+1')
        return result

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # Remember that if |state| is an end state, you should return an empty list [].
    def succAndProbReward(self, state, action):
        result = []
        if self.isEnd(state):
            return result
        if action == '-1':
            # Result 1
            newState = state - 1
            prob = .8
            reward = -5
            if newState == -2:
                reward = 20
            result.append((newState, prob, reward))
            # Result 2
            newState = state + 1
            prob = .2
            reward = -5
            if newState == 2:
                reward = 100
            result.append((newState, prob, reward))
        elif action == '+1':
            # Result 1
            newState = state + 1
            prob = .7
            reward = -5
            if newState == 2:
                reward = 100
            result.append((newState, prob, reward))
            # Result 2
            newState = state - 1
            prob = .3
            reward = -5
            if newState == -2:
                reward = 20
            result.append((newState, prob, reward))
        return result

    # Set the discount factor (float or integer) for your counterexample MDP.
    def discount(self):
        return 1.

def test1a():
    print('1a')
    mdp = BasicGameMDP()
    mdp.computeStates()
    algorithm = ValueIterationIters()
    
    def printResults(numIters):
        algorithm.solve(mdp, numIters)
        print(algorithm.V)
        print(algorithm.pi)

    for i in range(3):
        printResults(i)

def test3a():
    print('3a')
    state = (0, None, (0, 0, 3))
    print(all(cardCount == 0 for cardCount in state[2]))
    tup = (1, 1, 1)
    result = list(tup)
    result[1] -= 1
    print(tuple(result))
    tup = (1, 2, 3)
    tup = None
    print(tup)

def test3b():
    def removeCardFromDeck(deckCardCounts, index):
        deckCardCounts = list(deckCardCounts)
        deckCardCounts[index] -= 1
        return tuple(deckCardCounts)

    print(removeCardFromDeck((1,1,1,1),1))

def test4c():
    counts = (3, 2, 0, 1)
    presence = tuple(int(count > 0) for count in counts)
    print(counts)
    print(presence)

if __name__ == '__main__':
    #test3a()
    #test3b()
    test4c()
