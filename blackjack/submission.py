import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    # Return a value of any type capturing the start state of the MDP.
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0
        # END_YOUR_CODE

    # Return a list of strings representing actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        result = ['']
        if not(state == 1 or state == -1):
            result.append('+1')
            result.append('-1')
        return result
        # END_YOUR_CODE

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # Remember that if |state| is an end state, you should return an empty list [].
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        result = []
        if not(state == 1 or state == -1):
            if action == '+1':
                # Result 1
                newState = state + 1
                prob = .2
                reward = 0
                if newState == 1:
                    reward = 100
                result.append((newState, prob, reward))
                # Result 2
                newState = state - 1
                prob = .8
                reward = 0
                result.append((newState, prob, reward))
            elif action == '-1':
                # Result 1
                newState = state - 1
                prob = .9
                reward = 0
                result.append((newState, prob, reward))
                # Result 2
                newState = state + 1
                prob = .1
                reward = 0
                if newState == 1:
                    reward = 100
                result.append((newState, prob, reward))
        return result
        # END_YOUR_CODE

    # Set the discount factor (float or integer) for your counterexample MDP.
    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 1.
        # END_YOUR_CODE

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        def removeCardFromDeck(deckCardCounts, index):
            deckCardCounts = list(deckCardCounts)
            deckCardCounts[index] -= 1
            return tuple(deckCardCounts)

        def checkForEndOfGame(totalCardValueInHand, deckCardCounts, numDeckCards):
            reward = 0
            if totalCardValueInHand > self.threshold: # check for bust
                deckCardCounts = None
            elif numDeckCards == 1: # no cards remaining
                reward = totalCardValueInHand
                deckCardCounts = None
            return (deckCardCounts, reward)

        result = []
        if state[2] == None: # end state
            return result
        numDeckCards = sum(state[2])
        if action == 'Take':
            if state[1] != None:
                totalCardValueInHand = state[0] + self.cardValues[state[1]]
                deckCardCounts = removeCardFromDeck(state[2], state[1])
                prob = 1.0
                deckCardCounts, reward = checkForEndOfGame(totalCardValueInHand, deckCardCounts, numDeckCards)
                newState = (totalCardValueInHand, None, deckCardCounts)
                result.append((newState, prob, reward))
            else:
                for i in range(len(state[2])):
                    if state[2][i] > 0:
                        totalCardValueInHand = state[0] + self.cardValues[i]
                        deckCardCounts = removeCardFromDeck(state[2], i)
                        prob = 1. * state[2][i] / numDeckCards
                        deckCardCounts, reward = checkForEndOfGame(totalCardValueInHand,
                                deckCardCounts, numDeckCards)
                        newState = (totalCardValueInHand, None, deckCardCounts)
                        result.append((newState, prob, reward))
        elif action == 'Peek':
            if state[1] != None:
                return result
            for i in range(len(state[2])):
                if state[2][i] > 0:
                    prob = 1. * state[2][i] / numDeckCards
                    reward = -self.peekCost
                    newState = (state[0], i, state[2])
                    result.append((newState, prob, reward))
        elif action == 'Quit':
            prob = 1.0
            reward = state[0]
            newState = (state[0], state[1], None)
            result.append((newState, prob, reward))
        return result
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action at least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    return BlackjackMDP(cardValues=[1, 5, 21], multiplicity=15, threshold=20, peekCost=1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        v = 0
        if newState != None:
            v = max(self.getQ(newState, action) for action in self.actions(newState))
        residual = self.getQ(state, action) - (reward + self.discount * v)
        featureVector = self.featureExtractor(state, action)
        for feature in featureVector:
            self.weights[feature[0]] -= self.getStepSize() * residual * feature[1]
        # END_YOUR_CODE

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

def simulate_QL_over_MDP(mdp, featureExtractor):
    # NOTE: adding more code to this function is totally optional, but it will probably be useful
    # to you as you work to answer question 4b (a written question on this assignment).  We suggest
    # that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    # and then print some stats comparing the policies learned by these two approaches.
    # BEGIN_YOUR_CODE
    mdp.computeStates()
    ql = QLearningAlgorithm(mdp.actions, mdp.discount(), featureExtractor)
    vi = ValueIteration()
    util.simulate(mdp, ql, 30000, verbose=False) # learn
    ql.explorationProb = 0 # no more exploration, just exploitation of learned policy
    vi.solve(mdp)
    numStates = 0
    numDiffs = 0
    for state in vi.pi:
        viAction = vi.pi[state]
        qlAction = ql.getAction(state)
        print "state = {:30} vi: {:5} ql: {:5}".format(state, viAction, qlAction)
        numStates += 1
        if viAction != qlAction:
            numDiffs += 1
    print("difference = %g%%" %(100. * numDiffs / numStates))
    # END_YOUR_CODE


############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs.
# (See identityFeatureExtractor() above for a simple example.)
# Include the following features in the list you return:
# -- Indicator for the action and the current total (1 feature).
# -- Indicator for the action and the presence/absence of each face value in the deck.
#       Example: if the deck is (3, 4, 0, 2), then your indicator on the presence of each card is (1, 1, 0, 1)
#       Note: only add this feature if the deck is not None.
# -- Indicators for the action and the number of cards remaining with each face value (len(counts) features).
#       Note: only add these features if the deck is not None.
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state

    # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
    features = []
    # Indicator for action and total
    featureKey = (action, total)
    featureValue = 1
    features.append((featureKey, featureValue))
    if counts != None:
        # Indicator for action and presence of each face value in deck
        presence = tuple(int(count > 0) for count in counts)
        featureKey = (action, presence)
        featureValue = 1
        features.append((featureKey, featureValue))
        # Indicators for action and number of cards remaining of face value
        for index in range(len(counts)):
            featureKey = (action, index, counts[index])
            featureValue = 1
            features.append((featureKey, featureValue))
    return features
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

def compare_changed_MDP(original_mdp, modified_mdp, featureExtractor):
    # NOTE: as in 4b above, adding more code to this function is completely optional, but we've added
    # this partial function here to help you figure out the answer to 4d (a written question).
    # Consider adding some code here to simulate two different policies over the modified MDP
    # and compare the rewards generated by each.
    # BEGIN_YOUR_CODE
    originalMDP.computeStates()
    vi = ValueIteration()
    vi.solve(originalMDP)

    frl = util.FixedRLAlgorithm(vi.pi)
    totalRewards = util.simulate(newThresholdMDP, frl, 30000, verbose=False)
    print("Case 1: Value iteration on originalMDP, simulate on newThresholdMDP")
    print("expected reward = %g" %(1. * sum(totalRewards) / len(totalRewards)))

    newThresholdMDP.computeStates()
    vi = ValueIteration()
    vi.solve(newThresholdMDP)

    frl = util.FixedRLAlgorithm(vi.pi)
    totalRewards = util.simulate(newThresholdMDP, frl, 30000, verbose=False)
    print("Case 2: Value iteration on newThresholdMDP, simulate on newThresholdMDP")
    print("expected reward = %g" %(1. * sum(totalRewards) / len(totalRewards)))

    ql = QLearningAlgorithm(originalMDP.actions, originalMDP.discount(), blackjackFeatureExtractor)
    util.simulate(originalMDP, ql, 30000, verbose=False) # learn
    ql.explorationProb = 0 # no more exploration, just exploitation of learned policy
    totalRewards = util.simulate(newThresholdMDP, ql, 30000, verbose=False) # learn
    print("Case 3: Q-learning on originalMDP, simulate on newThresholdMDP")
    print("expected reward = %g" %(1. * sum(totalRewards) / len(totalRewards)))
    
    ql = QLearningAlgorithm(originalMDP.actions, originalMDP.discount(), blackjackFeatureExtractor)
    util.simulate(newThresholdMDP, ql, 30000, verbose=False) # learn
    ql.explorationProb = 0 # no more exploration, just exploitation of learned policy
    totalRewards = util.simulate(newThresholdMDP, ql, 30000, verbose=False) # learn
    print("Case 4: Q-learning on newThresholdMDP, simulate on newThresholdMDP")
    print("expected reward = %g" %(1. * sum(totalRewards) / len(totalRewards)))
    # END_YOUR_CODE

