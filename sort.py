import multiprocessing
from functools import reduce
import time
from functions import gaussianRandom as gss
from functions import decorator as dec

class Sort:
  def __init__(self, **kwargs):
    self.threads = kwargs['threads'] if 'threads' in kwargs else 1

  # Abstracta polimorfica entre tipos de sorting
  def sortMe(self, arr):
    pass

  # Devuelve el tamaño de cada parte del array que surge de dividir el mismo en la cantidad de procesos
  def _chunkSize(self, arr) -> int:
    return (len(arr) // self.threads) if self.threads > 1 else len(arr)

  # Genera las partes del array para enviar a cada procesador si se usa más de un procesador
  def _generateChunks(self, arr) -> list:
    return [arr[i:i + self._chunkSize(arr)] for i in range(0, len(arr), self._chunkSize(arr))] if self._chunkSize(arr) > 1 else arr

  # Cambia el methodo de sort inical
  def changeMethod(self, method):
    self.sortMethod = method

  # Inicia el sort
  def run(self, arr):
    with multiprocessing.Pool(processes=self.threads) as pool:
      sorted_chunks = pool.map(self.sortMe, self._generateChunks(arr))
    return self._joinChunks(sorted_chunks)

  # Combina las partes de la lista ya ordenadas
  def _joinChunks(self, chunks: list) -> list:
    return reduce(lambda res, sublist: self._merge(res, sublist), chunks[1:], chunks[0])

  # Une las listas ordenadas
  def _merge(self, left: list, right: list) -> list:
    i = j = 0
    result = []

    # Combinar las dos listas ordenadas
    while i < len(left) and j < len(right):
      if left[i] < right[j]:
        result.append(left[i])
        i += 1
      else:
        result.append(right[j])
        j += 1

    # Agregar los elementos restantes de ambas listas
    result.extend(left[i:])
    result.extend(right[j:])
    return result


class MergeSort(Sort):
  def sortMe(self, arr):
    return self._mergeSort(arr)

  # Devuelve el indice del medio del array
  def middle(self, arr):
    return len(arr) // 2

  # Devuelve la parte izquierda del array
  def left(self, arr):
    return arr[:self.middle(arr)]

  # Devuelve la parte derecha del array
  def right(self, arr):
    return arr[self.middle(arr):]

  def _mergeSort(self, arr):
    if not len(arr) > 1:
      return arr

    parts = [self.left(arr), self.right(arr)]
    parts = [self._mergeSort(part) for part in parts]
    return self._merge(*parts)


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


if __name__ == "__main__":
  # lista a ordenar
  data = gss(300000)
  
  t1 = time.perf_counter()
  sortedArray = MergeSort(threads = 4).run(data)
  t2 = time.perf_counter()

  dec(100)
  print(sortedArray[:20])
  dec(100)
  print(f"Time taken: {t2 - t1:.6f} seconds")
  dec(100)
