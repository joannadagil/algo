def bubbleSort1(arr):
    swaps = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        swaps += 1
    return swaps


def bubbleSort2(arr):
    swaps = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        swaps += 1
        if not swapped:
            break
    return swaps

arr1, arr2 = [64,32,52,16,13], [64,32,52,16,13]

print("Unsorted array is:", arr1)
print("Swaps:", bubbleSort1(arr1))
print("Sorted array is:", arr1)
print("Swaps:", bubbleSort2(arr2))
print("Sorted array is:", arr2)
