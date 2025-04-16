"""

Quick Sort is a divide-and-conqeur sorting algorithm that can be implemented iteratively or recursively. This algorithm finds correct index of a single element, the pivot, by 
using a two-pointer method to establish that all elements to the left are less than the pivot and all elements to the right are greater. Once a pivot is put in it's correct place,
it then sorts the sublists to the left and right. Because each traversal sorts the list slightly, the average Time Complexity is O(nlog(n)), and the space complexity is O(n).

"""

from utils.wrappers import wrap_sort

# Median of three function
def median_of_three(l, r, arr):
    m = ((r - l) // 2) + l              # Calculate middle index
    a, b, c = arr[l], arr[m], arr[r]    # Initialize left, middle, and right elements for comparison
    
    # Find and return the median index
    if (a <= b <= c) or (a >= b >= c):
        return m
    elif (b <= c <= a) or (b >= c >= a):
        return r
    else:
        return l

# Swap elements at indicies l and r
def swap(l, r, arr):
    arr[l], arr[r] = arr[r], arr[l]

# Quick Sort algorithm | Approach: Iterative, Time Complexity: Avg O(nlog(n)) Worst O(n^2), Space Complexity: Avg O(log(n)) Worst O(n)
@wrap_sort
def isort(arr):
    size = len(arr)
    queue = [(0, size-1)] # Initialize queue of left and right bound pairs, starting with full list bounds

    # Traverse and pop the queue until it is empty
    while queue:

        start, stop = queue.pop()                   # Initialize the start and stop indicies
        sub_size = stop - start

        # Base Cases: If the sublist has 2 or fewer elements, sort if needed and skip the current iteration
        if sub_size <= 0:
            continue
        if sub_size == 1:
            if arr[start] > arr[stop]:
                swap(start, stop, arr)
            continue

        pivot = median_of_three(start, stop, arr)   # Initialize pivot to the median of three of the left, middle, and right element of the sublist

        if pivot != start:
            swap(pivot, start, arr)                 # Swap the pivot and the first element if necessary

        pivot = start    # Set the pivot index to the first element
        left = start+1   # Set the left pointer to the second element
        right = stop     # Set the right pointer to the last element

        # Loop until the pointers cross
        while left <= right:
            
            # While left pointer is in bounds and element is not greater than the pivot, increment the pointer
            while left < size and arr[left] <= arr[pivot]:
                left += 1

            # While right pointer is in bounds and element is not less than the pivot, decrement the pointer
            while right > 0 and arr[right] >= arr[pivot]:
                right -= 1

            # Swap the left and right elements if the bounds haven't crossed
            if left <= right:
                swap(left, right, arr)

        swap(pivot, right, arr) # Once bounds have crossed, swap the elements at the pivot index and right pointer
        
        # Append the left and right sublist indicies to the queue
        queue.insert(0, (start, right-1))
        queue.insert(0, (left, stop))

    return arr

# Quick Sort algorithm | Approach: Recursive, Time Complexity: Avg O(nlog(n)) Worst O(n^2), Space Complexity: O(n)
@wrap_sort
def rsort(arr):

    def recur(arr):
        size = len(arr)
        start, stop = 0, size-1    # Initialize start and stop indicies

        # If list has three elements, sort and return
        if size == 3:
            median = median_of_three(start, stop, arr)
            return [min(arr), arr[median], max(arr)]
        # If list has two elements, sort and return
        if size == 2:
            if arr[0] > arr[1]:
                swap(0, 1, arr)
            return arr
        # If list has one element, return it
        if size <= 1:
            return arr

        pivot = median_of_three(start, stop, arr)   # Initialize pivot as median of three

        # If the pivot is not the first element, switch the pivot with the first element
        if pivot != start:
            swap(pivot, start, arr)

        pivot = start    # Set the pivot index to the first element
        left = start+1   # Set the left pointer to the second element
        right = stop     # Set the right pointer to the last element

        # Loop until the pointers cross
        while left <= right:
            
            # Increment the left pointer until an element greater than the pivot is found
            while left < size and arr[left] <= arr[pivot]:
                left += 1

            # Decerement the right pointer until an element less than the pivot is found
            while right > 0 and arr[right] >= arr[pivot]:
                right -= 1

            # Swap the left and right elements if the bounds haven't crossed
            if left <= right:
                swap(left, right, arr)

        swap(pivot, right, arr) # Once bounds have crossed, swap the pivot and right elements
            
        # Sort the left and right sublists
        sub_left = recur(arr[:right])
        sub_right = recur(arr[left:])
        
        # Return the sorted sublists with the pivot inbetween
        return sub_left+[arr[right]]+sub_right
    
    return recur(arr)