def print_hi(name):
    print("Hi, {0}!".format(name))

def insertion_sort(arr):
    swaps =0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        arr[j + 1] = key
    return swaps

# [0 1 2 3 4]
#  x   x
#    x   x

#      x   x
#  x   x

#        x  x
#    x   x



# n = 5
# gap = n//2 = 2
# j = 2, i = 0

# j = 3, i = 1

# j = 4, i = 2, i = 0
# j = 5, i = 3, i = 1

# gap = 1
# 


def shell_sort(arr):
    swaps = 0
    n = len(arr)
    gap = n // 2
    while gap > 0:
        j = gap
        while j < n:
            i = j - gap
            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swaps += 1
                i = i - gap
            j += 1
        gap = gap // 2
    return swaps

def hibbard_sort(arr):
    swaps = 0
    n = len(arr)
    loops = 0
    gap = 2^loops - 1
    while gap < n:
        j = gap
        while j > n:
            i = j - gap
            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swaps += 1
                i = i - gap
            j -= 1
        loops += 1
        gap = 2^loops - 1
    return swaps

arr = [12, 11, 13, 5, 6, 7, 1, 3, 9, 10, 2, 4, 8]
print("swaps in shell:     ", shell_sort(arr))
arr2 = [12, 11, 13, 5, 6, 7, 1, 3, 9, 10, 2, 4, 8]
print("swaps in insertion: ", insertion_sort(arr2))
arr3 = [12, 11, 13, 5, 6, 7, 1, 3, 9, 10, 2, 4, 8]
print("swaps in hibbard: ", hibbard_sort(arr3))

for i in range(len(arr)):
    print("%d" % arr[i], end=" ")
print()

for i in range(len(arr2)):
    print("%d" % arr2[i], end=" ")
print()

if __name__ == '__main__':
    print_hi('PyCharm')


# 0 1 2 3 4 5 6 7 8 9 
# 

# sedgewick na zad dodatkowe