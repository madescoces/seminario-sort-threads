import threading
import random
import time

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def multi_threaded_merge_sort(arr, num_threads):
    if num_threads <= 1:
        return merge_sort(arr)
    # Divide the input list into equal-sized sublists
    size = len(arr) // num_threads
    sublists = [arr[i:i+size] for i in range(0, len(arr), size)]
    
    # Create threads for sorting each sublist
    threads = []
    sorted_sublists = []
    for sublist in sublists:
        thread = threading.Thread(target=lambda sublist: sorted_sublists.append(merge_sort(sublist)), args=(sublist,))        
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:        
        thread.start()
    
    for thread in threads:        
        thread.join()

    # Merge the sorted sublists
    merged = sorted_sublists[0]
    for sublist in sorted_sublists[1:]:
        merged = merge(merged, sublist)
    return merged

# Example usage
input_list = [0] * 2000000
for i in range(2000000):
	input_list[i] = random.random()*10

num_threads = 6
print("Original List:", input_list[:50] )

t1 = time.perf_counter()

sorted_list = multi_threaded_merge_sort(input_list, num_threads)

t2 = time.perf_counter()

print("Sorted list:", sorted_list[:50])

print(f"Time taken: {t2 - t1:.6f} seconds")


