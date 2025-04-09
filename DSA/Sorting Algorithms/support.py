# This file contains the support functions used by the sorting algorithms.

from random import randint
from time import time

# Generate a list of random integers. num_range=(lower_limit, upper_limit), length=length
def gen_arr(**kwargs):
    left, right = kwargs.get("num_range", (0, 100))            # Default range is 0-100
    length = kwargs.get("length", 20)                        # Default length is 20
    return [randint(left, right) for _ in range(length)]

# Wrapper for sorting algorithms that prints the list before and after sorting, and tracks the runtime of the function
def show_stats(func):
    def wrapper(*args, **kwargs):

        print("\nSorting:", args[0])
        start = time()*1000                 # Start time (milliseconds)
        new_arr = func(*args, **kwargs)
        end = time()*1000                   # End time (milliseconds)
        print("\nSorted: ", new_arr)
        
        print("\nRuntime:", end-start)      # Runtime
    
    return wrapper