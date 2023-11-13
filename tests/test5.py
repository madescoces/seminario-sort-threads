import numpy as np

data = [4, 2, 7, 1, 9, 3, 6, 8, 5, 0]
chunk_size = 3

# Crear un array NumPy directamente
numpy_array = np.array(data).reshape(-1, chunk_size)

# Imprimir el array NumPy resultante
print(numpy_array)
