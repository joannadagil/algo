'''
BUCKETSORT
wykorzystuje algorytm sortowania wewnątrz swoich kubełków 


'''
import random
import time

def insertSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def bucketSort(arr):
    if len(arr) == 0:
        return arr
    temp = []
    buckets = 10
    # range = (max-min)/buckets
    # bucket_index = int((arr[i] - min)/range)
    for i in range(buckets):
        temp.append([])
    for j in arr:
        index = int(buckets * j)
        #if index == buckets:
        #    index -= 1
        temp[index].append(j)
    for i in range(buckets):
        insertSort(temp[i])
    k=0
    for i in range(buckets):
        for j in range(len(temp[i])):
            arr[k] = temp[i][j]
            k += 1
    return arr
    


for i in range(5):
    print("---------Test", i+1, "---------")

    a = int(input("podaj dlugosc: "))

    arr1 = [random.random() for _ in range(a)]
    arr2 = arr1.copy()

    time1 = time.time()
    bucketSort(arr1)
    time2 = time.time()
    arr2.sort()
    time3 = time.time()

    print("Czas bucketSort(): ", (time2 - time1)*1000000)
    print("Czas quickSort():  ", (time3 - time2)*1000000)
    #print(arr1)
    #print(arr2)


    