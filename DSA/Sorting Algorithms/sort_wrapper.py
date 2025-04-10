# This file contains the support functions used by the sorting algorithms.

from random import randint
from time import time

# Generate a list of random integers. num_range=(lower_limit, upper_limit), length=length
def gen_arr(**kwargs):
    left, right = kwargs.get("num_range", (0, 100))          # Default range is 0-100
    length = kwargs.get("length", 20)                        # Default length is 20
    return [randint(left, right) for _ in range(length)]

# Wrapper for sorting algorithms that passes the function a random list by default, prints the list before and after sorting, and tracks the runtime of the function
def wrap_sort(func):
    def wrapper(unsorted_arr=None, *args, **kwargs):

        print(f"\n\n{kwargs.get('title', '')}\n")   # Print function title if provided

        # Generate a random list if none is provided
        if not unsorted_arr:
            unsorted_arr = gen_arr(**kwargs)    # Keyword arguments are passed to the list generator

        print("\nSorting:", unsorted_arr)
        
        start = time()*1000                     
        new_arr = func(unsorted_arr, *args)     # Arguments are passed to the sort function
        end = time()*1000                       
        
        print("\nSorted: ", new_arr)
        print("\nRuntime:", end-start)          # Runtime
    
    return wrapper