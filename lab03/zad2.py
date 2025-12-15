def bidisort(arr):
    # bidirectional bubble sort
    n = len(arr)
    start = 0
    end = n - 1 
    swapped = True

    while swapped:
        swapped = False

        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end, start, -1):
            if arr[i-1] > arr[i]:
                arr[i-1], arr[i] = arr[i], arr[i-1]
                swapped = True

        start += 1

    return arr

arr = [64, 34, 25, 12, 22, 11, 90]
print("Unsorted array is:", arr)
bidisort(arr)
print("Sorted array is:", arr)

