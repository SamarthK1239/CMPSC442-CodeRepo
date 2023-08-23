############################################################
# CMPSC 442: Meeting 2 Activity (Python #1)
############################################################
############################################################
# Section 1: Dictionaries
#
# First illustration of the utility of zip(); also very useful
# with higher order functions
#
############################################################
# The function assemble_dict should return a dictionary using
# the ordered list 'dictkeys' as the dictionary keys and the
# ordered list 'dictvalues' as the corresponding values. If the
# two lists are not the same length, the longer list is truncated
# to an equal length by dropping the excess items from the end.
# Note that assemble_dict can be defined in one line using the python
# function zip(), and that append_dict can use a dictionary method called
# update()

def assemble_dict(dictkeys, dictvalues):
    keys_length = len(dictkeys)
    values_length = len(dictvalues)
    if keys_length > values_length:
        dictkeys = dictkeys[:values_length]
    elif values_length > keys_length:
        dictvalues = dictvalues[:keys_length]
    return dict(zip(dictkeys, dictvalues))


def append_dict(dict1, dict2):
    dict1.update(dict2)
    return dict1


############################################################
# Section 2: Sequence slicing (making copies)
#
# Recall that the slice parameters take on sensible default
# values when omitted. In some cases, it may be necessary to use
# the optional third parameter to specify a step size.
############################################################
# The function copy(mylist, add) should return a tuple (mylist, newlist)
# where newlist is a shallow copy of the original mylist and where add
# is appended to mylist
def copy(mylist, new):
    return mylist, mylist + [new]


# The function all_but_last(seq) should return a new sequence
# containing all but the last element of the input sequence.
# If the input sequence is empty, a new empty sequence of the same type
# should be returned.
def all_but_last(seq):
    if len(seq) == 0:
        return seq
    return seq[:-1]


# The function every_other(seq) should return a new sequence
# containing every other element of the input sequence, starting
# with the first. Hint: This function can be written in one
# line using the optional third parameter of the slice notation.
def every_other(seq):
    return seq[::2]

