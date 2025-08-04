import sys

def leer_barrios(archivo_barrios):
    with open(archivo_barrios, 'r', encoding='utf-8') as f:
        lineas = f.read().split('\n')

    separador = lineas.index('')
    norte = lineas[:separador]
    sur = lineas[separador+1:]
    return norte, sur

def leer_propuestas(archivo_propuestas):
    propuestas = []
    with open(archivo_propuestas, 'r', encoding='utf-8') as f:
        for linea in f:
            if ',' in linea:
                norte, sur = [s.strip() for s in linea.strip().strip(".").split(',')]
                propuestas.append((norte, sur))
    return propuestas

def max_puentes(barrios_norte, barrios_sur, propuestas):
    
    orden_norte = {nombre: i for i, nombre in enumerate(barrios_norte)}
    orden_sur = {nombre: i for i, nombre in enumerate(barrios_sur)}

    propuestas_ordenadas = sorted(propuestas, key=lambda x: orden_norte[x[0]])
    
    # Inicializo la lista que contendrá los índices del sur
    secuencia = []

    # Recorro las propuestas ordenadas por barrio norte
    for propuesta in propuestas_ordenadas:
        barrio_sur = propuesta[1]
    
        indice_sur = orden_sur[barrio_sur]
    
        secuencia.append(indice_sur)

    # Buscamos la secuencia creciente más larga en la secuencia de índices del sur (LIS)
    n = len(secuencia)
    dp = [1] * n
    prev = [-1] * n

    for i in range(n):
        for j in range(i):
            if secuencia[j] < secuencia[i] and dp[j] + 1 > dp[i]: # Comprobamos si la secuencia es creciente y si se puede aumentar la longitud (si es más larga que la que teníamos en ese punto)
                dp[i] = dp[j] + 1 # Actualizamos la longitud de la secuencia
                prev[i] = j # Guardamos el índice del anterior para reconstruir la secuencia

    # Buscamos la posición con mayor longitud
    max_len = max(dp)
    idx = dp.index(max_len)

    # Reconstruimos la solución
    indices_solucion = []
    while idx != -1:
        indices_solucion.append(idx)
        idx = prev[idx]

    indices_solucion.reverse()

    propuestas_finales = [propuestas_ordenadas[i] for i in indices_solucion]
    return propuestas_finales

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python puentes_dp.py barrios.txt propuestas.txt")
        sys.exit(1)

    archivo_barrios = sys.argv[1]
    archivo_propuestas = sys.argv[2]

    norte, sur = leer_barrios(archivo_barrios)
    propuestas = leer_propuestas(archivo_propuestas)

    resultado = max_puentes(norte, sur, propuestas)

    print(len(resultado))

    for norte, sur in resultado:
        print(f"{norte}, {sur}")