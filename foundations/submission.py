import collections
import math

############################################################
# Problem 3a

def findAlphabeticallyLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    words = text.split()
    return max(words)
    # END_YOUR_CODE

############################################################
# Problem 3b

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return math.sqrt((loc2[0] - loc1[0])**2 + (loc2[1] - loc1[1])**2)
    # END_YOUR_CODE

############################################################
# Problem 3c

def mutateSentences(sentence):
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be similar to the original sentence if
      - it as the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the original sentence
        (the words within each pair should appear in the same order in the output sentence
         as they did in the orignal sentence.)
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more than
        once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']
                (reordered versions of this list are allowed)
    """
    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    originalSentence = sentence.split()
    # build dictionary storing a word's predecessors and followers
    words = {}
    for index in range(len(originalSentence)):
        if not(originalSentence[index] in words): # add word if not already in dictionary
            words[originalSentence[index]] = (set(), set())
        if index != 0: # append preceding word to word's preceding list
            words[originalSentence[index]][0].add(originalSentence[index-1])
        if index != len(originalSentence) - 1: # append following word word's following list
            words[originalSentence[index]][1].add(originalSentence[index+1])

    phrases = collections.deque()
    for word in words:
        phrases.append([word])

    if len(phrases) == 0:
        return []

    phrase = phrases.popleft()
    while len(phrase) < len(originalSentence):
        lastWord = phrase[-1]
        for followingWord in words[lastWord][1]:
            newPhrase = list(phrase)
            newPhrase.append(followingWord)
            phrases.append(newPhrase)
        phrase = phrases.popleft()

    output = [' '.join(phrase)]
    while len(phrases) > 0:
        phrase = phrases.popleft()
        output.append(' '.join(phrase))

    return output
    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    dotProduct = 0
    for key in v1:
        dotProduct += v1[key] * v2[key]
    return dotProduct
    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    allKeys = list(set(v1.keys()) | set(v2.keys()))
    for key in allKeys:
        v1[key] += scale * v2[key]
    # END_YOUR_CODE

############################################################
# Problem 3f

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    You might find it useful to use collections.defaultdict(int).
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    words = text.split()
    counter = collections.Counter(words)
    singletons = set()
    for key in counter:
        if counter[key] == 1:
            singletons.add(key)
    return singletons
    # END_YOUR_CODE

############################################################
# Problem 3g
def computeLongestPalindromeLength_v1(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (our solution is 19 lines of code, but don't worry if you deviate from this)
    if len(text) == 0:
        return 0
    if len(text) == 1:
        return 1
    if text == text[::-1]:
        return len(text)

    # find duplicate characters
    duplicateCharacters = []
    counter = collections.Counter(text)
    for character in counter:
        if counter[character] >= 2:
            duplicateCharacters.append(character)

    if len(duplicateCharacters) == 0:
        return 1

    # create remnant strings by removing duplicates at end
    remnants = []
    for character in duplicateCharacters:
        remnants.append(text[text.find(character)+1:text.rfind(character)])

    maxLength = 0
    for remnant in remnants:
        length = computeLongestPalindromeLength(remnant) + 2
        if length > maxLength:
            maxLength = length

    return maxLength
    # END_YOUR_CODE
############################################################
# Problem 3g
def computeLongestPalindromeLength(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (our solution is 19 lines of code, but don't worry if you deviate from this)
    cache = {}
    
    def removeChar(txt, index):
        return txt[:index] + txt[index+1:]

    def computeLengthRecursively(txt, firstIndex, lastIndex):
        if txt in cache:
            return cache[txt]
        elif txt == txt[::-1]:
            result = len(txt)
        elif txt[firstIndex] == txt[lastIndex]:
            result = computeLengthRecursively(txt, firstIndex+1, lastIndex-1)
        else:
            len1 = computeLengthRecursively(removeChar(txt, firstIndex), firstIndex, lastIndex-1)
            len2 = computeLengthRecursively(removeChar(txt, lastIndex), firstIndex, lastIndex-1)
            result =  max(len1,len2)
        
        cache[txt] = result
        return result

    return computeLengthRecursively(text, 0, len(text)-1)
    # END_YOUR_CODE
