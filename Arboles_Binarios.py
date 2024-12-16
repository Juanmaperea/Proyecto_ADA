
# Segunda estrategia usadar: Arboles Binarios
import os
import time
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class Nodo:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, data, key):
        nuevo_nodo = Nodo(key, data)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_rec(self.raiz, nuevo_nodo)

    def _insertar_rec(self, actual, nuevo):
        if nuevo.key > actual.key:
            if actual.right is None:
                actual.right = nuevo
            else:
                self._insertar_rec(actual.right, nuevo)
        else:
            if actual.left is None:
                actual.left = nuevo
            else:
                self._insertar_rec(actual.left, nuevo)

    def en_orden(self):
        resultados = []
        self._en_orden_rec(self.raiz, resultados)
        return resultados

    def _en_orden_rec(self, actual, resultados):
        if actual is not None:
            self._en_orden_rec(actual.right, resultados)
            resultados.append(actual.data)
            self._en_orden_rec(actual.left, resultados)

class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

class Pregunta:
    def __init__(self, id):
        self.id = id
        self.encuestados = ArbolBinario()

    def agregar_encuestado(self, encuestado):
        key = (encuestado.opinion, encuestado.experticia)
        self.encuestados.insertar(encuestado, key)

    def promedio_opinion(self):
        encuestados = self.encuestados.en_orden()
        return round(sum(e.opinion for e in encuestados) / len(encuestados), 2)

    def promedio_experticia(self):
        encuestados = self.encuestados.en_orden()
        return round(sum(e.experticia for e in encuestados) / len(encuestados), 2)

    def lista_encuestados(self):
        return self.encuestados.en_orden()

class Tema:
    def __init__(self, id):
        self.id = id
        self.preguntas = ArbolBinario()

    def agregar_pregunta(self, pregunta):
        key = pregunta.promedio_opinion()
        self.preguntas.insertar(pregunta, key)

    def lista_preguntas(self):
        return self.preguntas.en_orden()


def cargar_datos_desde_txt(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe. Verifica la ruta y vuelve a intentarlo.")

    encuestados = []
    temas = {}
    encuestado_id = 1
    preguntas = []

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    tema_actual = None
    tema_id = 1
    pregunta_bloque = []

    for linea in lineas:
        linea = linea.strip()

        # Procesar encuestados
        if re.match(r".+, Experticia: \d+, Opinión: \d+", linea):
            partes = re.split(r", Experticia: |, Opinión: ", linea)
            nombre = partes[0]
            experticia = int(partes[1])
            opinion = int(partes[2])
            encuestados.append(Encuestado(encuestado_id, nombre, experticia, opinion))
            encuestado_id += 1

        # Procesar preguntas
        elif re.match(r"^\{.+\}$", linea):
            encuestados_ids = list(map(int, linea.strip("{} ").split(", ")))
            pregunta_bloque.append(encuestados_ids)

        # Cambio de tema
        elif linea == "" and pregunta_bloque:
            if tema_actual is None:
                tema_actual = Tema(f"Tema {tema_id}")
                temas[f"Tema {tema_id}"] = tema_actual

            for i, encuestados_ids in enumerate(pregunta_bloque):
                pregunta = Pregunta(f"{tema_actual.id.split()[-1]}.{i + 1}")
                for encuestado_id in encuestados_ids:
                    pregunta.agregar_encuestado(next(e for e in encuestados if e.id == encuestado_id))
                tema_actual.agregar_pregunta(pregunta)

            tema_id += 1
            tema_actual = None
            pregunta_bloque = []

    if pregunta_bloque:
        if tema_actual is None:
            tema_actual = Tema(f"Tema {tema_id}")
            temas[f"Tema {tema_id}"] = tema_actual

        for i, encuestados_ids in enumerate(pregunta_bloque):
            pregunta = Pregunta(f"{tema_actual.id.split()[-1]}.{i + 1}")
            for encuestado_id in encuestados_ids:
                pregunta.agregar_encuestado(next(e for e in encuestados if e.id == encuestado_id))
            tema_actual.agregar_pregunta(pregunta)

    return encuestados, temas

def guardar_resultados_en_txt(ruta_salida, temas, encuestados):
    with open(ruta_salida, 'w', encoding='utf-8') as archivo:
        archivo.write("Resultados de la encuesta:\n\n")

        temas_ordenados = sorted(temas.items(), key=lambda x: -sum(p.promedio_opinion() for p in x[1].lista_preguntas()) / len(x[1].lista_preguntas()))

        for tema_id, tema in temas_ordenados:
            promedio_tema = round(sum(p.promedio_opinion() for p in tema.lista_preguntas()) / len(tema.lista_preguntas()), 2)
            archivo.write(f"[{promedio_tema}] {tema_id}:\n")
            for pregunta in tema.lista_preguntas():
                archivo.write(f" [{pregunta.promedio_opinion():.2f}] Pregunta {pregunta.id}: {tuple(e.id for e in pregunta.lista_encuestados())}\n")

        archivo.write("\nLista de encuestados:\n")
        for encuestado in sorted(encuestados, key=lambda e: (-e.experticia, -e.id)):
            archivo.write(f" ({encuestado.id}, Nombre:'{encuestado.nombre}', Experticia:{encuestado.experticia}, Opinión:{encuestado.opinion})\n")

        # Calcular estadísticas adicionales
        preguntas = [p for tema in temas.values() for p in tema.lista_preguntas()]
        pregunta_max_opinion = max(preguntas, key=lambda p: p.promedio_opinion())
        pregunta_min_opinion = min(preguntas, key=lambda p: p.promedio_opinion())
        pregunta_max_experticia = max(preguntas, key=lambda p: p.promedio_experticia())
        pregunta_min_experticia = min(preguntas, key=lambda p: p.promedio_experticia())
        encuestado_max_opinion = max(encuestados, key=lambda e: e.opinion)
        encuestado_min_opinion = min(encuestados, key=lambda e: e.opinion)
        encuestado_max_experticia = max(encuestados, key=lambda e: (e.experticia, e.opinion, -e.id))
        encuestado_min_experticia = min(encuestados, key=lambda e: (e.experticia, -e.opinion, e.id))

        archivo.write("\nResultados:\n")
        archivo.write(f"  Pregunta con mayor promedio de opinion: [{pregunta_max_opinion.promedio_opinion()}] Pregunta: {pregunta_max_opinion.id}\n")
        archivo.write(f"  Pregunta con menor promedio de opinion: [{pregunta_min_opinion.promedio_opinion()}] Pregunta: {pregunta_min_opinion.id}\n")
        archivo.write(f"  Pregunta con mayor promedio de experticia: [{pregunta_max_experticia.promedio_experticia()}] Pregunta: {pregunta_max_experticia.id}\n")
        archivo.write(f"  Pregunta con menor promedio de experticia: [{pregunta_min_experticia.promedio_experticia()}] Pregunta: {pregunta_min_experticia.id}\n")
        archivo.write(f"  Encuestado con mayor opinion: ({encuestado_max_opinion.id}, Nombre:'{encuestado_max_opinion.nombre}', Experticia:{encuestado_max_opinion.experticia}, Opinión:{encuestado_max_opinion.opinion})\n")
        archivo.write(f"  Encuestado con menor opinion: ({encuestado_min_opinion.id}, Nombre:'{encuestado_min_opinion.nombre}', Experticia:{encuestado_min_opinion.experticia}, Opinión:{encuestado_min_opinion.opinion})\n")
        archivo.write(f"  Encuestado con mayor experticia: ({encuestado_max_experticia.id}, Nombre:'{encuestado_max_experticia.nombre}', Experticia:{encuestado_max_experticia.experticia}, Opinión:{encuestado_max_experticia.opinion})\n")
        archivo.write(f"  Encuestado con menor experticia: ({encuestado_min_experticia.id}, Nombre:'{encuestado_min_experticia.nombre}', Experticia:{encuestado_min_experticia.experticia}, Opinión:{encuestado_min_experticia.opinion})\n")
        archivo.write(f"  Promedio de experticia de los encuestados: {round(sum(e.experticia for e in encuestados) / len(encuestados), 2)}\n")
        archivo.write(f"  Promedio de opinion de los encuestados: {round(sum(e.opinion for e in encuestados) / len(encuestados), 2)}\n")



# Función para seleccionar archivo de entrada
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccione el archivo de entrada",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    entrada_var.set(archivo)

# Función para guardar resultados
def guardar_resultados():
    archivo_entrada = entrada_var.get()
    archivo_salida = salida_var.get()
    if not archivo_entrada or not archivo_salida:
        messagebox.showerror("Error", "Debe seleccionar un archivo de entrada y definir el archivo de salida.")
        return

    try:
        encuestados, temas = cargar_datos_desde_txt(archivo_entrada)
        guardar_resultados_en_txt(archivo_salida, temas, encuestados)
        messagebox.showinfo("Éxito", f"Resultados guardados en {archivo_salida}")
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"No se encontró el archivo: {e}")
    except ValueError as e:
        messagebox.showerror("Error", f"Error al procesar el archivo: {e}")

# Configuración de la interfaz gráfica
def interfaz_grafica():
    global entrada_var, salida_var

    ventana = tk.Tk()
    ventana.title("Procesador de Encuestas")
    ventana.geometry("500x300")
    ventana.resizable(False, False)

    entrada_var = tk.StringVar()
    salida_var = tk.StringVar()

    tk.Label(ventana, text="Archivo de entrada:", font=("Arial", 12)).pack(pady=10)
    entrada_frame = tk.Frame(ventana)
    entrada_frame.pack()
    tk.Entry(entrada_frame, textvariable=entrada_var, width=40, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(entrada_frame, text="Seleccionar", command=seleccionar_archivo).pack(side=tk.LEFT)

    tk.Label(ventana, text="Nombre del archivo de salida (con extensión .txt):", font=("Arial", 12)).pack(pady=10)
    tk.Entry(ventana, textvariable=salida_var, width=40, font=("Arial", 10)).pack(pady=5)

    tk.Button(ventana, text="Guardar Resultados", command=guardar_resultados, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)

    ventana.mainloop()


# Función para leer parámetros desde archivo
def leer_parametros(archivo):
    parametros = {}
    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            for linea in f:
                key, value = linea.strip().split('=')
                parametros[key.strip()] = value.strip()
    return parametros

# Función principal adaptada
def main():
    tiempo_inicial = time.time()

    # Leer archivo de parámetros
    archivo_parametros = 'parametros.txt'
    parametros = leer_parametros(archivo_parametros)
    
    # Obtener nombres de archivo
    archivo_entrada = parametros.get('archivo_entrada')
    archivo_salida = parametros.get('archivo_salida')


    # Cargar datos y procesar
    encuestados, temas = cargar_datos_desde_txt(archivo_entrada)
    guardar_resultados_en_txt(archivo_salida, temas, encuestados)
    print("Procesamiento completado. Los resultados se han guardado en 'Salidas'.")

    # Medir tiempo de ejecución
    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicial
    print(f"El tiempo total de ejecución es: {tiempo_total:.4f} segundos.")

if __name__ == "__main__":
    #interfaz_grafica()
    # Alternativamente, llama a main() directamente para pruebas sin GUI
    main()





