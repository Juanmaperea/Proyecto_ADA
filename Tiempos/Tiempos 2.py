import matplotlib.pyplot as plt

# Datos de la tabla (valores de la imagen proporcionada)
n_encuestados = [12, 20, 40, 53, 89, 118, 150]
tiempos_listas = [0.0071108341217041016, 0.0010085105895996094, 0.010785818099975586, 
                  0.011560440063476562, 0.014025449752807617, 0.014826536178588867, 
                  0.014112224769592285]
tiempos_arboles_binarios = [0.002, 0.019, 0.012, 0.011, 0.01, 0.012, 0.02]

# Crear el gráfico
plt.figure(figsize=(10, 6))
plt.plot(n_encuestados, tiempos_listas, marker='o', label="Listas", color='orange')
plt.plot(n_encuestados, tiempos_arboles_binarios, marker='s', label="Árboles Binarios", color='blue')

# Etiquetas y título
plt.xlabel("Nº de Encuestados")
plt.ylabel("Tiempo (segundos)")
plt.title("Comparación de Tiempos: Listas vs Árboles Binarios")
plt.legend()
plt.grid()

# Mostrar el gráfico
plt.show()