import sys
from collections import OrderedDict

DEBUG = False  # Se activa si se pasa el flag -d

def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def leer_ofertas(path):
    with open(path, 'r') as f:
        lineas = [line.strip() for line in f.readlines() if line != '\n']
    m = int(lineas[0])  # cantidad de porciones
    ofertas = {}
    for linea in lineas[1:]:
        partes = linea.split(',')
        nombre = partes[0]
        ofertas[nombre] = list(map(int, partes[1:]))
    return m, ofertas

def leer_enemigos(path):
    enemigos = {}
    with open(path, 'r') as f:
        for linea in f:
            partes = linea.strip().split(',')
            nombre = partes[0]
            enemigos[nombre] = set(partes[1:]) if len(partes) > 1 else set()
    return enemigos

def normalizar(solucion):
    # Buscamos índices donde el invitado NO es VACIO
    indices_validos = [i for i in range(len(solucion)) if solucion[i] != "__VACIO__"]
    
    # Si está todo vacío, devolvemos tal cual
    if not indices_validos:
        return tuple(solucion)

    # Elegimos el índice del menor alfabético real
    min_i = min(indices_validos, key=lambda i: solucion[i])
    return tuple(solucion[min_i:] + solucion[:min_i])

# Copia un OrderedDict manteniendo el orden y borra la clave en la copia
def eliminar_clave_y_devolver_nuevo_ordered_dict(original, clave):
    nuevo = OrderedDict(original)
    if clave != VACIO: # Vacio es la unica clave que puede reaparecer varias veces en la solucion
        del nuevo[clave]
    return nuevo

def backtrack(m, invitados, enemigos):
    soluciones = []
    soluciones_vistas = set()

    def bt(parcial, disponibles):
        if len(parcial) == m:
            a = parcial[-1]
            b = parcial[0]
            if a != VACIO and b != VACIO and (b in enemigos[a] or a in enemigos[b]):
                return

            norm = normalizar(parcial)
            if norm not in soluciones_vistas:
                soluciones.append(list(norm))
                soluciones_vistas.add(norm)
                debug_print(f"\n[SOLUCIÓN VÁLIDA N°{len(soluciones_vistas)}] {norm}")
            return

        # Elegir de los disponibles reales
        for inv in disponibles:
            if parcial:
                anterior = parcial[-1]
                if anterior != VACIO and inv != VACIO and (inv in enemigos[anterior] or anterior in enemigos[inv]):
                    continue

            parcial.append(inv)
            bt(parcial, eliminar_clave_y_devolver_nuevo_ordered_dict(disponibles,inv))
            parcial.pop()

    bt([], OrderedDict.fromkeys(invitados + [VACIO]))
    return soluciones

def mejor_rotacion_y_ganancia(solucion, ofertas):
    m = len(solucion)
    cont = 0
    max_ganancia = -1
    mejor_rot = []
    for r in range(m):
        if cont == 0:
            debug_print(f"\nInicio Prueba Rotaciones con {solucion}")
            cont += 1
        rotada = solucion[r:] + solucion[:r]
        ganancia = sum(ofertas[invitado][i] for i, invitado in enumerate(rotada))
        debug_print(f"[ROTACIÓN] {rotada} => Ganancia: {ganancia}")
        if ganancia > max_ganancia:
            max_ganancia = ganancia
            mejor_rot = rotada
    return mejor_rot, max_ganancia

# MAIN
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python subasta_bt.py ofertas.txt enemigos.txt")
        sys.exit(1)

    archivo_ofertas = sys.argv[1]
    archivo_enemigos = sys.argv[2]

    if "-d" in sys.argv:
        DEBUG = True

    m, ofertas = leer_ofertas(archivo_ofertas)
    VACIO = "__VACIO__"
    ofertas[VACIO] = [0] * m  # Ganancia 0 en cualquier posición para VACIO


    enemigos = leer_enemigos(archivo_enemigos)
    invitados = list(ofertas.keys())

    soluciones = backtrack(m, invitados, enemigos)

    mejor_ganancia = -1
    mejor_distribucion = []

    for s in soluciones:
        rotacion, ganancia = mejor_rotacion_y_ganancia(s, ofertas)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_distribucion = rotacion

    print("\n======= RESULTADO FINAL =======")
    if mejor_distribucion:
        print(f"La ganancia máxima a obtener es: {mejor_ganancia}")
        print(f"Los invitados ganadores son: {', '.join(mejor_distribucion)}")
    else:
        print("No se encontró ninguna asignación válida.")
