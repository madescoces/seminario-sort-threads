import multiprocessing
import random
import time
import numpy as np

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


def merge_sort_parallel(data, processes=4):
  # Dividir la lista en segmentos para cada núcleo
  chunk_size = len(data) // processes
  chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
 
  # Crear un pool de procesos
  with multiprocessing.Pool(processes=processes) as pool:
    # Aplicar merge_sort a cada segmento de manera paralela
    sorted_chunks = pool.map(merge_sort, chunks)

  # Combinar los resultados de cada núcleo
  result = sorted_chunks[0]
  for sublist in sorted_chunks[1:]:
    result = merge(result, sublist)
  return result


def merge_sort(data):
  if len(data) <= 1:
    return data

  # Dividir la lista en dos mitades
  mid = len(data) // 2
  left = data[:mid]
  right = data[mid:]

  # Ordenar recursivamente cada mitad
  left = merge_sort(left)
  right = merge_sort(right)

  # Combinar las dos mitades ordenadas
  return merge(left, right)


def merge(left, right):
  result = []
  i = j = 0

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





if __name__ == "__main__":
  # Ejemplo de uso
  data = gaussianRandom(1000000)
  t1 = time.perf_counter()  
  sorted_data = merge_sort_parallel(data)
  t2 = time.perf_counter()

  #print("Lista ordenada:", sorted_data[:20])
  print()
  print(f"Time taken: {t2 - t1:.6f} seconds")
