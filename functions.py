from enum import Enum
import threading
import numpy as np
import random

# Función para generar un array de gaussianos


def gaussianRandom(n: int) -> np.array:
  # Genera los números base
  uniform = [random.random() for _ in range(n * 2)]

  # Aplicar transformación inversa para obtener la distribución gaussiana
  # formula:  squareroot(-2ln(U))*cos(2πV)
  # donde U y V son números aleatorios y Z es es número aleatorio Gaussiano
  # uniform[::2] obtiene todos los números en posición par
  # uniform[1::2] obtiene todos los números en posición impar
  gaussian = [np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * v)
              for u, v in zip(uniform[::2], uniform[1::2])]

  return gaussian


def arrMiddle(arr):
  middle = len(arr) // 2
  return middle


def arrFirstHalf(arr):
  return arr[:arrMiddle(arr)]


def arrSecondHalf(arr):
  return arr[arrMiddle(arr):]


def merge(left, right):
  arr = [0] * len(left + right)

  # i = indice left array, j = indice right array, k = indice array a ordenar
  index = {'i': 0, 'j': 0, 'k': 0}

  # Incrementa el indice i, j y k
  def increase(key: str):
    try:
      index[key] += 1
    except IndexError:
      print(f"Error: index '{index}' not found")

  while index['i'] < len(left) and index['j'] < len(right):
    arr[index['k']] = left[index['i']] if left[index['i']] < right[index['j']] else right[index['j']]
    increase('i') if left[index['i']] < right[index['j']] else increase('j')
    increase('k')

  def step(key: str, part):
    while index[key] < len(part):
      arr[index['k']] = part[index[key]]
      increase(key)
      increase('k')

  step('i', left)
  step('j', right)
  return arr


def sortThreaded(arr,  _sortType=None, threads=2):
  sortType = _sortType if _sortType else MergeSort()  

  if threads <= 1:
    return sortType.sortMe(arr)

  sublists = []
  size = len(arr) // threads
  for i in range(0, len(arr), size):
    sublists.append(arr[i:i + size])

  sorted_sublists = []
  threads = []

  if threads != 0:    
    for sublist in sublists:
      thread = threading.Thread(target=lambda sublist: sorted_sublists.append(sortType.sortMe(sublist)), args=(sublist,))
      threads.append(thread)
    
    for thread in threads:
      thread.start()

    for thread in threads:
      thread.join()

    merged = sorted_sublists[0]
    for sublist in sorted_sublists[1:]:
      merged = merge(merged, sublist)
    return merged  

  left_half = sortThreaded(arrFirstHalf(arr))
  right_half = sortThreaded(arrSecondHalf(arr))

  return merge(left_half, right_half)


class Sort:
  def sortMe(self, arr):
    pass


class MergeSort(Sort):
  def sortMe(self, arr):
    return self._mergeSort(arr)

  def _mergeSort(self, arr):    
    if not len(arr) > 1:
      return arr
    
    parts = [arrFirstHalf(arr), arrSecondHalf(arr)]
    parts = [self._mergeSort(part) for part in parts]
    return merge(*parts)
  
class BubbleSort(Sort):
  def sortMe(self, arr):
    if not len(arr) > 1:
      return arr

    n = len(arr)
    swapped = False
    
    for i in range(n - 1):
      for j in range(0, n - i - 1):
        if arr[j] > arr[j + 1]:
          swapped = True
          arr[j], arr[j + 1] = arr[j + 1], arr[j]

      if not swapped:
        return arr
    
    return arr

class QuickSort(Sort):
  def sortMe(self, arr):    
    return self._quicksort(arr)

  def _quicksort(self, arr):       
    if not len(arr) > 1:
      return arr
    
    pivot = arr[0]
    lesser = [x for x in arr[1:] if x <= pivot]
    greater = [x for x in arr[1:] if x > pivot]
    return self._quicksort(lesser) + [pivot] + self._quicksort(greater)


# data = gaussianRandom(40000)

# arr = sortThreaded(data, MergeSort(), 4)

# print(arr[:20])


# t1 = time.perf_counter()

# sorted_list = multi_threaded_merge_sort(input_list, num_threads)

# t2 = time.perf_counter()

# print("Sorted list:", sorted_list[:50])

# print(f"Time taken: {t2 - t1:.6f} seconds")

