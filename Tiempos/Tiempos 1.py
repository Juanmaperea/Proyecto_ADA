import time
import random
import matplotlib.pyplot as plt
import numpy as np

# Función principal del Merge Sort:
def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key)
    right = merge_sort(arr[mid:], key=key)
    return merge(left, right, key)

# Función auxiliar Merge del Merge Sort:
def merge(left, right, key):
    sorted_list = []
    while left and right:
        if key(left[0]) < key(right[0]):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left if left else right)
    return sorted_list

# Configuración del experimento
sizes = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
execution_times = []
theoretical_times = []

for size in sizes:
    # Generar una lista aleatoria de tamaño 'size'
    random_list = [random.randint(0, 10000) for _ in range(size)]
    
    # Medir tiempo de ejecución del Merge Sort
    start_time = time.perf_counter()
    merge_sort(random_list)
    end_time = time.perf_counter()
    
    execution_time = end_time - start_time
    execution_times.append(execution_time)
    
    # Calcular complejidad teórica O(nlog(n))
    theoretical_time = size * np.log2(size)
    theoretical_times.append(theoretical_time)

# Normalizar los tiempos teóricos para compararlos con los reales
normalized_theoretical_times = [t / max(theoretical_times) * max(execution_times) for t in theoretical_times]

# Generar la gráfica
plt.figure(figsize=(10, 6))
plt.plot(sizes, execution_times, label="Tiempo real (Merge Sort)", marker='o')
plt.plot(sizes, normalized_theoretical_times, label="T(n) = O(n log n) (normalizado)", linestyle='--', color='red')
plt.xlabel("Tamaño de la lista (n)")
plt.ylabel("Tiempo (segundos)")
plt.title("Comparación de tiempos reales vs complejidad teórica en Merge Sort")
plt.legend()
plt.grid()
plt.show()