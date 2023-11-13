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

def decorator(number:int):  
  lines = ''.join(['-' for _ in range(number)])
  print(f"\n{lines}\n")
  
