############################################################
# CMPSC 442: Meeting 3 Activity (Python #2)
############################################################
############################################################
# Section 1: List comprehension
############################################################
# Consider the function extract_and_apply(l,p,f) shown below, which
# extracts the elements of a list l satisfying a boolean predicate p,
# applies a function f to each such element, and returns the result.
# def extract_and_apply(l, p, f):
# result = []
# for x in l:
# if p(x):
# result.append(f(x))
# return result
# Rewrite extract_and_apply(l, p, f) in one line using a
# list comprehension. For testing either definition of
# extract_and_apply, consider using lambda expressions for
# the second and third arguments (i.e., anonymous functions).
def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]


# Write a function concatenate(seqs) that returns a list
# containing the concatenation of the elements of the input sequences.
# Use a single list comprehension, in one line.
def concatenate(seqs):
    return [x for seq in seqs for x in seq]


# Assume the input matrix is a list of same-length lists. Transpose
# of a matrix is defined as swapping its rows with its columns:
# meaning first row becomes first column, and so forth.
# [[1, 2], [3, 4], [5, 6]] transposed is [1, 3, 5], [2, 4, 6].
# Given a correct definition of transpose, then
# matrix[i][j] == transpose(matrix)[j][i]. NOTE: A one line
# definition can be written using zip().
def transpose(matrix):
    return [list(x) for x in zip(*matrix)]
