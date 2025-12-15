import random
import time

def bubbleSort(arr):
    swaps = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
    return swaps


def selectionSort(arr):
    swaps = 0
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return swaps

def hybridSort(arr):
    threshold = 30
    if len(arr) <= threshold:
        swaps = bubbleSort(arr)
    else:
        swaps = selectionSort(arr)
    return swaps

for i in range(5):
    print("---------Test", i+1, "---------")
    arr1 = random.sample(range(1, 100), random.randint(20, 100))
    arr2 = arr1.copy()
    arr3 = arr1.copy()
    print("array length:", len(arr1))
    time1 = time.perf_counter_ns()
    print("hybridSort swaps:", hybridSort(arr1))
    time2 = time.perf_counter_ns()
    print("time:", (time2 - time1)/1000)
    time3 = time.perf_counter_ns()
    print("bubbleSort swaps:", bubbleSort(arr2))
    time4 = time.perf_counter_ns()
    print("time:", (time4 - time3)/1000)
    time5 = time.perf_counter_ns()
    print("selectionSort swaps:", selectionSort(arr3))
    time6 = time.perf_counter_ns()
    print("time:", (time6 - time5)/1000)

    