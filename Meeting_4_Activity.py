############################################################
# CMPSC 442: Meeting 4 Activity (Combinatorics; Text
# Processing)
############################################################
############################################################
# Section 1: Combinatorial Algorithms
# Implement all of these as generators, meaning use the yield
# keyword instead of return
############################################################
# The prefixes of a sequence are to include the empty sequence,
# the first element, the first two elements, etc., up to and
# including the full sequence itself.
def prefixes(seq):
    for i in range(len(seq)):
        yield seq[:i + 1]


# The suffixes of a sequence are to include the empty sequence,
# the last element, the last two elements, etc., up to and
# including the full sequence itself.
def suffixes(seq):
    for i in range(len(seq)):
        yield seq[-i - 1:]


# Output should be all non-empty slices of the input sequence.
def slices(seq):
    for i in range(len(seq)):
        for j in range(i + 1, len(seq) + 1):
            yield seq[i:j]


############################################################
# Section 2: Text Processing
############################################################
# Convert the input text string to lowercase, with words separated
# by only a single space, removing all extra leading, trailing, or
# inter-word spaces.
def normalize(text):
    return ' '.join(text.lower().split())


# Remove all the vowels from the input string.
def no_vowels(text):
    vowels = 'aeiou'
    return ''.join([x for x in text if x not in vowels])


# Extract all digits in the input string and return them as spelled out words
# each separated by a single space. If there are no digits in the input string,
# return the empty string.
def digits_to_words(text):
    digits = 'zero one two three four five six seven eight nine'.split()
    return ' '.join([digits[int(x)] for x in text if x.isdigit()])


# In computer programming, there are many naming conventions for variables. Two that are
# widely used are as follows: 1) words in a variable name are separated using underscores,
# 2) words in a variable name are written as a single word in mixed case meaning the first
# word is written in lowercase, all the rest are capitalized. Write a function
# that converts a variable name from the former convention to the latter. Leading and
# trailing underscores should be ignored. A variable name consisting solely of underscores
# should be converted to the empty string.
def to_mixed_case(name):
    if name.count('_') == len(name):
        return ''
    return ''.join([x.capitalize() for x in name.split('_') if x != ''])