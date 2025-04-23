# This file contains the support functions used by solutions and sorting algorithms.

from random import randint
from time import time

# Generate a list of random integers. num_range=(lower_limit, upper_limit), length=length
def gen_arr(**kwargs):
    left, right = kwargs.get("num_range", (0, 100))          # Default range is 0-100
    length = kwargs.get("length", 20)                        # Default length is 20
    return [randint(left, right) for _ in range(length)]

def timer(func):
    def wrapper(*args):

        start = time()
        output = func(*args)
        stop = time()

        print(f"Runtime: {round((stop-start)*1000, 5)}ms")

        return output

    return wrapper

# Wrapper for sorting algorithms that passes the function a random list by default, prints the list before and after sorting, and tracks the runtime of the function
def wrap_sort(func):
    def wrapper(unsorted_arr=None, *args, **kwargs):

        print(f"\n\n{kwargs.get('title', '')}\n")   # Print function title if provided

        # Generate a random list if none is provided
        if not unsorted_arr:
            unsorted_arr = gen_arr(**kwargs)    # Keyword arguments are passed to the list generator

        print("\nSorting:", unsorted_arr)
        
        start = time()                    
        new_arr = func(unsorted_arr, *args)     # Arguments are passed to the sort function
        end = time()                     
        
        print("\nSorted: ", new_arr)
        print(f"\nRuntime: {round((end-start)*1000, 5)}ms")          # Runtime
    
    return wrapper