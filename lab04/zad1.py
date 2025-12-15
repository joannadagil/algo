'''
HEAPSORT
sortowanie kopców binarnych - wszystkie poziomy oprócz ostatniego są wypełnione
maxheap/minheap - rodzic jest większy/mniejszy od dzieci

0  1  2  3  4 
4 10  3  5  1 

     4
 10      3
5  1

'''
import random
import time

# kopcowanie
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapify_min(arr, n, i):
    smallest = i

    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] < arr[smallest]:
        smallest = left
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify_min(arr, n, smallest)

def heapify_3way(arr, n, i):
    largest = i

    left = 3 * i + 1
    mid = 3 * i + 2
    right = 3 * i + 3

    if left < n and arr[left] > arr[largest]:
        largest = left
    if mid < n and arr[mid] > arr[largest]:
        largest = mid
    if right < n and arr[right] > arr[largest]:
        largest = right 

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_3way(arr, n, largest)

def heapSort_3way(arr):
    n = len(arr)

    for i in range(n // 3 - 1, -1, -1):
        heapify_3way(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify_3way(arr, i, 0)

def heapSort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def quickSort(arr):
    if len(arr) <=


for i in range(5):
    print("---------Test", i+1, "---------")

    a = int(input("podaj dlugosc: "))

    arr1 = random.sample(range(1, 100), a)
    arr2 = arr1.copy()

    time1 = time.time()
    heapSort(arr1)
    time2 = time.time()
    arr2.sort()
    time3 = time.time()

    print("Czas heapSort(): ", (time2 - time1)*1000000)
    print("Czas quickSort(): ", (time3 - time2)*1000000)
    #print(arr1)
    #print(arr2)


    