from asyncio import sleep
from typing import Dict
import threading
import numpy as np
import random

def gaussianRandom(n:int) -> np.array:
  # Genera los números base
  uniform = [random.random() for _ in range(n*2)] 
    
  # Aplicar transformación inversa para obtener la distribución gaussiana
  # formula:  squareroot(-2ln(U))*cos(2πV) 
  # donde U y V son números aleatorios y Z es es número aleatorio Gaussiano 
  # uniform[::2] obtiene todos los números en posición par
  # uniform[1::2] obtiene todos los números en posición impar
  gaussian = [np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * v) for u, v in zip(uniform[::2], uniform[1::2])]

  return gaussian

def arrMiddle(arr):
  middle = len(arr) // 2  
  return middle

def arrFirstHalf(arr):
  return arr[:arrMiddle(arr)]

def arrSecondHalf(arr):
  return arr[arrMiddle(arr):]

def increase(dic: Dict[str, int] ,index:str):
  try:
    dic[index] += 1
  except IndexError:
    print(f"Error: index '{index}' not found")

def step(_i:int, _k:int, arr, part):
  while i < len(part):
    arr[_k] = part[_i]
    i += 1
    k += 1

def merge(arr, parts):
  index = {'i': 0,'j': 0,'k': 0}

  left = parts[0]
  right = parts[1]  

  while index['i'] < len(left) and index['j'] < len(right):
    #print("entro en el while largo")
    #arr[k] = left[i] if left[i] < right[j] else right[j]    
    increase(i) if left[i] < right[j] else increase(j)
    
    k += 1
    
    
    print("i vale",i)
    print("j vale",j)
    print("k vale",k)

  step(i,k,arr,left)
  step(j,k,arr,right)

def mergeSort(arr):
  if len(arr) <= 1:
    return arr
  
  threads = {}
  
  parts = [arrFirstHalf(arr), arrSecondHalf(arr)]
  
  # Crea los hilos
  for i, part in enumerate(parts):    
    threads[i] = threading.Thread(target=mergeSort, args=(part,))
  
  # Dispara los hilos
  [threads[th].start() for th in threads]

  # Espera a que finalicen todos para unirlos
  [threads[th].join() for th in threads]
  
  merge(arr, parts)


data = gaussianRandom(10)
mergeSort(data)