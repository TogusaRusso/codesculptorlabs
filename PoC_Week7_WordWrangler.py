"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(120)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2 = []
    for item in list1:
        if not list2:
            list2.append(item)
        elif item <> list2[-1]:
            list2.append(item)
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list3 = []
    for item in list1:
        if item in list2:
            list3.append(item)
    return list3

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    list3 = []
    len1 = len(list1)
    len2 = len(list2)
    ptr1 = 0
    ptr2 = 0
    while ptr1 < len1 or ptr2 < len2:
        if   ptr1 == len1:
            list3.extend(list2[ptr2:])
            ptr2 = len2
        elif ptr2 == len2:
            list3.extend(list1[ptr1:])
            ptr1 = len1
        elif list1[ptr1] > list2[ptr2]:
            list3.append(list2[ptr2])
            ptr2 += 1
        else:
            list3.append(list1[ptr1])
            ptr1 += 1
    return list3
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    num = len(list1) 
    if num < 2:
        return list1
    else:
        mid = num / 2
        return merge(merge_sort(list1[:mid]),
                     merge_sort(list1[mid:]))
     

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    num = len(word)
    if num == 0:
        return [""]
    first = word[0]
    rest_strings = gen_all_strings(word[1:])
    result = list(rest_strings)
    for rest in rest_strings:
        if rest == "":
            result.append(first);
        else:
            for pos in xrange(len(rest) + 1):
                result.append(rest[:pos] 
                              + first + rest[pos:])
    return result

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    result = []
    for line in netfile.readlines():
        result.append(line.rstrip())
    return result

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
