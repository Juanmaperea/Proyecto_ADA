# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# SE IMPORTAN LOS PAQUETES NECESARIOS PARA EL DESARROLLO DEL PROYECTO:# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/



import re
import time
import os



# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# SE DEFINEN LAS FUNCIONES AUXILIARES PARA EL DESARROLLO DEL PROYECTO:# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/



# SE DEFINEN FUNCIONES PARA REALIZAR EL ORDENAMIENTO USANDO EL ALGORITMO DEL MERGE SORT:

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



# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# SE DEFINEN LAS CLASES PARA LOS DISTINTOS ELEMENTOS QUE CONFORMAN LA ENCUESTA:# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/



# SE DEFINE UNA CLASE PARA LOS ENCUESTADOS:
class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):

        # Se inicializan los atributos de la clase:
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

    # Se redefine la representación de una instancia de la clase Encuestado:
    def __repr__(self):
        return f"[{self.id}, {self.nombre}, {self.experticia}, {self.opinion}]"



# SE DEFINE UNA CLASE PARA LAS PREGUNTAS:
class Pregunta:
    def __init__(self, id, pregunta):

        # Se inicializan los atributos de la clase:
        self.pregunta = pregunta
        self.id = id

        # Se define una lista para guardar encuestados; es decir, las personas que dieron su opinión al respecto:
        self.encuestados = [] 

    # Se agregan encuestados a la lista definida anteriormente:
    def agregar_encuestado(self, encuestado):
        self.encuestados.append(encuestado)

    # Se calcula la opinión promedio por pregunta:
    def opinion_promedio(self):
        if not self.encuestados:
            return 0
        promedio_opinion = sum(encuestado.opinion for encuestado in self.encuestados) / len(self.encuestados)
        return promedio_opinion
    
    # Se calcula la experticia promedio por pregunta:
    def experticia_promedio(self):
        if not self.encuestados:
            return 0
        promedio_experticia = sum(encuestado.experticia for encuestado in self.encuestados) / len(self.encuestados)
        return promedio_experticia

    # Se ordenan los encuestados de acuerdo a su opinión y su experticia en la pregunta:
    def ordenar_encuestados(self):
        self.encuestados = merge_sort(self.encuestados, key=lambda e: (-e.opinion, -e.experticia))

    # Se redefine la representación de una instancia de la clase Pregunta:
    def __repr__(self):
        return f"[{self.id}, {self.pregunta}, {self.encuestados}]"



# SE DEFINE UNA CLASE PARA LOS TEMAS:
class Tema:
    def __init__(self, id, tema):

        # Se inicializan los atributos de la clase:
        self.id = id
        self.tema = tema

        # Se define una lista para guardar las preguntas; es decir, las preguntas que hacen parte del tema:
        self.preguntas = []

    # Se agregan preguntas a la lista definida anteriormente:
    def agregar_pregunta(self, pregunta):
        self.preguntas.append(pregunta)

    # Se calcula la opinión promedio por tema:
    def opinion_promedio(self):
        if not self.preguntas:
            return 0
        
        promedio_total = 0

        for pregunta in self.preguntas:
            promedio_total += pregunta.opinion_promedio()

        return promedio_total / len(self.preguntas) if self.preguntas else 0
    
    # Se calcula la experticia promedio por tema:
    def experticia_promedio(self):
        if not self.preguntas:
            return 0
        
        experticia_total = 0

        for pregunta in self.preguntas:
            experticia_total += pregunta.experticia_promedio()

        return experticia_total / len(self.preguntas) if self.preguntas else 0

    # Se ordenan las preguntas de acuerdo a su opinión promedio, su experticia promedio y su número de encuestados:
    def ordenar_preguntas(self):
        self.preguntas = merge_sort(self.preguntas, key=lambda p: (-p.opinion_promedio(), -p.experticia_promedio(), -len(p.encuestados)))

    # Se redefine la representación de una instancia de la clase Tema:
    def __repr__(self):
        self.ordenar_preguntas()

        resultados = [f"[{self.opinion_promedio():.2f}] Tema {self.id}: "]

        for i, pregunta in enumerate(self.preguntas, start=1):
            pregunta.ordenar_encuestados()
            resultados.append(
                f" [{pregunta.opinion_promedio():.2f}] Pregunta {pregunta.id}: " "(" + ", ".join(str(encuestado.id) for encuestado in pregunta.encuestados) + ")"
            )

        return "\n".join(resultados)



# SE DEFINE UNA CLASE PARA LAS ENCUESTAS:
class Encuesta:
    def __init__(self):

        # Se define una lista para guardar los temas; es decir, las temas que hacen parte de la encuesta:
        self.temas = []

    # Se agregan temas a la lista definida anteriormente:
    def agregar_tema(self, tema):
        self.temas.append(tema)

    # Se ordenan los temas de acuerdo a su opinión promedio, su experticia promedio y su número de encuestados:
    def ordenar_temas(self):
        self.temas = merge_sort(self.temas, key=lambda t: (-t.opinion_promedio(), -t.experticia_promedio(), -sum(len(p.encuestados) for p in t.preguntas)))

    # Se ordenan los encuestados de acuerdo a su opinión:
    def ordenar_encuestados(self):
        todos_encuestados = [encuestado for tema in self.temas for pregunta in tema.preguntas for encuestado in pregunta.encuestados]
        return merge_sort(todos_encuestados, key=lambda e: (-e.experticia, -e.id))

    # Se calculan estadísticas:
    def calcular_estadisticas(self):
        todos_preguntas = [pregunta for tema in self.temas for pregunta in tema.preguntas]
        todos_encuestados = [encuestado for tema in self.temas for pregunta in tema.preguntas for encuestado in pregunta.encuestados]

        pregunta_promedio_mayor_opinion = max(todos_preguntas, key=lambda p: p.opinion_promedio(), default=None)
        pregunta_promedio_menor_opinion = min(todos_preguntas, key=lambda p: p.opinion_promedio(), default=None)
        pregunta_promedio_mayor_experticia = max(todos_preguntas, key=lambda p: p.experticia_promedio(), default=None)
        pregunta_promedio_menor_experticia = min(todos_preguntas, key=lambda p: p.experticia_promedio(), default=None)

        encuestado_promedio_mayor_opinion = max(todos_encuestados, key=lambda e: e.opinion, default=None)
        encuestado_promedio_menor_opinion = min(todos_encuestados, key=lambda e: e.opinion, default=None)
        encuestado_promedio_mayor_experticia = max(todos_encuestados, key=lambda e: e.experticia, default=None)
        encuestado_promedio_menor_experticia = min(todos_encuestados, key=lambda e: e.experticia, default=None)

        encuestado_promedio_total_opinion = sum(encuestado.opinion for encuestado in todos_encuestados) / len(todos_encuestados)
        encuestado_promedio_total_experticia = sum(encuestado.experticia for encuestado in todos_encuestados) / len(todos_encuestados)

        resultado = [pregunta_promedio_mayor_opinion, pregunta_promedio_menor_opinion, 
                     pregunta_promedio_mayor_experticia, pregunta_promedio_menor_experticia,
                     encuestado_promedio_mayor_opinion, encuestado_promedio_menor_opinion,
                     encuestado_promedio_mayor_experticia, encuestado_promedio_menor_experticia,
                     encuestado_promedio_total_opinion, encuestado_promedio_total_experticia]

        return resultado

    # Se redefine la representación de una instancia de la clase Encuesta:
    def __repr__(self):
        self.ordenar_temas()
        lista_encuestados = self.ordenar_encuestados()
        estadisticas = self.calcular_estadisticas()

        resultados = []

        resultados.append("Resultados de la encuesta:")
        resultados.append("")
        
        for tema in self.temas:
            resultados.append(str(tema))
            resultados.append("")

        resultados.append("Lista de encuestados:")
        for encuestado in lista_encuestados:
            resultados.append(f" ({encuestado.id}, Nombre:'{encuestado.nombre}', Experticia:{encuestado.experticia}, Opinión:{encuestado.opinion})")
        resultados.append("")

        resultados.append("Resultados:")
        resultados.append(f"  Pregunta con mayor promedio de opinion: [{estadisticas[0].opinion_promedio():.2f}] Pregunta: {estadisticas[0].id}")
        resultados.append(f"  Pregunta con menor promedio de opinion: [{estadisticas[1].opinion_promedio():.2f}] Pregunta: {estadisticas[1].id}")
        resultados.append(f"  Pregunta con mayor promedio de experticia: [{estadisticas[2].experticia_promedio():.2f}] Pregunta: {estadisticas[2].id}")
        resultados.append(f"  Pregunta con menor promedio de experticia: [{estadisticas[3].experticia_promedio():.2f}] Pregunta: {estadisticas[3].id}")
        
        resultados.append(f"  Encuestado con mayor opinion: ({estadisticas[4].id} , Nombre: {estadisticas[4].nombre} , Experticia: {estadisticas[4].experticia}, Opinion: {estadisticas[4].opinion})")
        resultados.append(f"  Encuestado con menor opinion: ({estadisticas[5].id} , Nombre: {estadisticas[5].nombre} , Experticia: {estadisticas[5].experticia}, Opinion: {estadisticas[5].opinion})")
        resultados.append(f"  Encuestado con mayor experticia: ({estadisticas[6].id} , Nombre: {estadisticas[6].nombre} , Experticia: {estadisticas[6].experticia}, Opinion: {estadisticas[6].opinion})")
        resultados.append(f"  Encuestado con menor experticia: ({estadisticas[7].id} , Nombre: {estadisticas[7].nombre} , Experticia: {estadisticas[7].experticia}, Opinion: {estadisticas[7].opinion})")
        
        resultados.append(f"  Promedio de experticia de los encuestados: {estadisticas[9]}")
        resultados.append(f"  Promedio de opinion de los encuestados: {estadisticas[8]:.2f}")

        return "\n".join(resultados)



# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# SE DEFINEN LAS FUNCIONES PARA IMPORTAR PARÁMETROS, DATOS DE ENTRADA Y SALIDA:# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/



# SE DEFINE UNA FUNCIÓN PARA LEER LOS PARÁMETROS DE UN ARCHIVO DE TEXTO:
def leer_parametros(archivo_parametros):
    parametros = {}
    with open(archivo_parametros, 'r', encoding='utf-8') as f:
        for linea in f:
            if "=" in linea:
                clave, valor = linea.strip().split('=')
                parametros[clave.strip()] = valor.strip()

    return parametros

# SE DEFINE UNA FUNCIÓN PARA LEER LOS DATOS DE ENTADA DE UN ARCHIVO DE TEXTO:
def leer_datos_entrada(archivo):
    encuestados = []
    temas = []
    with open(archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    # Se procesan los encuestados:
    i = 0
    while i < len(lineas) and lineas[i].strip():
        partes = lineas[i].strip().split(", ")
        nombre = partes[0]
        experticia = int(partes[1].split(": ")[1])
        opinion = int(partes[2].split(": ")[1])
        encuestados.append(Encuestado(i + 1, nombre, experticia, opinion))
        i += 1

    # Procesar los temas y las preguntas:
    tema_id = 1
    while i < len(lineas):
        # Agrupar líneas de un tema (separadas por dobles saltos de línea)
        bloque_tema = []
        while i < len(lineas) and lineas[i].strip():
            bloque_tema.append(lineas[i].strip())
            i += 1
        
        # Saltar líneas en blanco entre temas
        while i < len(lineas) and not lineas[i].strip():
            i += 1

        # Crear un tema si el bloque no está vacío
        if bloque_tema:
            tema = Tema(tema_id, f"Tema {tema_id}")
            pregunta_id = 1
            
            for pregunta_linea in bloque_tema:
                ids_encuestados = eval(pregunta_linea)  # Convertir texto a lista de IDs
                pregunta = Pregunta(f"{tema_id}.{pregunta_id}", f"Pregunta {pregunta_id}")
                
                for id_encuestado in ids_encuestados:
                    encuestado = next(e for e in encuestados if e.id == id_encuestado)
                    pregunta.agregar_encuestado(encuestado)
                
                tema.agregar_pregunta(pregunta)
                pregunta_id += 1

            temas.append(tema)
            tema_id += 1

    # Crear la instancia de la encuesta:
    encuesta = Encuesta()
    for tema in temas:
        encuesta.agregar_tema(tema)

    return encuesta



# SE DEFINE UNA FUNCIÓN PARA GUARDAR LOS DATOS DE SALIDA EN UN ARCHIVO DE TEXTO:
def guardar_resultados_salida(nombre_salida, encuesta):
    nombre_archivo = nombre_salida
    
    # Se abre el archivo para guardar los resultados:
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(str(encuesta))
        f.write("\n")



# FUNCIÓN PRINCIPAL PARA EJECUTAR EL CÓDIGO:
def main():

    # Se inicia a contar el tiempo de ejecución:
    tiempo_inicial = time.time()

    # Se leen los parámetros:
    archivo_parametros = 'parametros.txt'
    parametros = leer_parametros(archivo_parametros)

    # Se obtienen los nombres de los archivos de entrada y salida desde el archivo de parámetros:
    archivo_entrada = parametros.get('archivo_entrada')
    archivo_entrada = "Entradas/" + archivo_entrada

    archivo_salida = parametros.get('archivo_salida')
    archivo_salida = "Salidas/" + archivo_salida

    # Se leen los datos de entrada desde el archivo:
    encuesta = leer_datos_entrada(archivo_entrada)

    # Se guardan los resultados en el archivo de salida
    guardar_resultados_salida(archivo_salida, encuesta)

    print(f"Procesamiento completado. Los resultados se han guardado en 'Salidas'.")

    # Se para el tiempo y se contabiliza:
    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicial
    print("El tiempo total de ejecución es: ", tiempo_total, "Segundos.")


if __name__ == "__main__":
    main()