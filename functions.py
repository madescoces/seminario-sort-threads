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


# saca el indice medio de un array
def arrMiddle(arr):
  middle = len(arr) // 2
  return middle

# Primer mitad del array
def arrFirstHalf(arr):
  return arr[:arrMiddle(arr)]

# Segunda mitad del array
def arrSecondHalf(arr):
  return arr[arrMiddle(arr):]

# Función que ordena
def merge(arr, parts):
  # i = indice left array, j = indice right array, k = indice array a ordenar
  index = {'i': 0, 'j': 0, 'k': 0}

  left = parts[0]
  right = parts[1]

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

# Función que dispara los threads para el sort
def mergeSort(arr):
  if len(arr) <= 1:
    return arr

  # diccionario con los 2 threads por cada división
  threads = {}

  # Array con ambas partes
  parts = [arrFirstHalf(arr), arrSecondHalf(arr)]

  # Crea los hilos
  for i, part in enumerate(parts):
    threads[i] = threading.Thread(target=mergeSort, args=(part,))

  # Dispara los hilos
  [threads[th].start() for th in threads]

  # Espera a que finalicen todos para unirlos
  [threads[th].join() for th in threads]

  merge(arr, parts)

def bubbleSort(arr):
	n = len(arr)
	swapped = False
	for i in range(n-1):
		for j in range(0, n-i-1):
			if arr[j] > arr[j + 1]:
				swapped = True
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
		
		if not swapped:
			return