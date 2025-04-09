"""

Bubble Sort is an iterative sorting algorithm that operates through pair swapping. The algorithm iterates each pair of elements in the list at index j and j+1. The elements are 
swapped if the left is greater than the right, until the algorithm reaches the end of the list. Each iteration of this algorithm scans from index 0 to index length-i, with i being 
the current iteration. This causes an average Time Complexity of (n^2 - n) / 2, which remains O(n^2), and because this algorithm sorts in-place, the Space Complexity is O(1).

"""

from support import gen_arr, show_stats

# Bubble Sort algorithm | Approach: Iterative, Time Complexity: O(n^2), Space Complexity: O(1)
@show_stats
def bubble_sort(arr):
    size = len(arr)
    
    # Repeat the algorithm n-1 times
    for i in range(size-1):
        
        swapped = False # Track if any swaps occur
        
        # Iterate through each pair in the remaining unsorted elements
        for j in range(size-i-1):
            
            # If the left element is greater than the right, swap the elements
            if arr[j] > arr[j+1]:
                
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True # Record that a swap occured
        
        # If no swaps occured, break (the list is sorted)
        if not swapped:
            break
    
    return arr

if __name__ == "__main__":
    
    elements = gen_arr() # List of random integers 0-100 of length 20

    print("\n\nBubble Sort:\n")
    bubble_sort(elements)