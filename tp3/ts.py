import random
import sys
from collections import defaultdict
from utils_inversores import *

ALFA = 0.5
BETA = 0.3
IT_TABU = 4  # Iteraciones durante las que un movimiento es tabú
MAX_ITERACIONES = 10

def buscar_mejor_vecino(S, Sm, I, W, incompatibles, DicTabu, freq, delta_acumulado):
    mejor_vecino = None
    mejor_score = float('-inf')
    movimientos_posibles = []

    for i in set(I) - S:
        movimientos_posibles.append((AGREGAR, i))
    for i in S:
        movimientos_posibles.append((QUITAR, i))
    for i in S:
        for j in set(I) - S:
            movimientos_posibles.append((INTERCAMBIAR, i, j))

    for m in movimientos_posibles:
        S_prime = set(S)

        if m[0] == AGREGAR:
            S_prime.add(m[1])
        elif m[0] == QUITAR:
            S_prime.remove(m[1])
        elif m[0] == INTERCAMBIAR:
            S_prime.remove(m[1])  # i
            S_prime.add(m[2])     # j

        if not es_factible(S_prime, incompatibles):
            continue

        Cv = suma_de_montos(S_prime, W)
        Cs = suma_de_montos(S, W)

        prohibido = m in DicTabu and DicTabu[m] > 0
        if prohibido and Cv <= suma_de_montos(Sm, W):
            continue

        max_freq = max(freq.values() or [1])
        max_delta = max([abs(d) for d in delta_acumulado.values()] or [1])

        intensificacion = delta_acumulado[m] / max_delta if max_delta else 0
        diversificacion = freq[m] / max_freq if max_freq else 0

        score = Cv + ALFA * intensificacion - BETA * diversificacion

        if score > mejor_score:
            mejor_score = score
            mejor_vecino = (set(S_prime), m, Cv - Cs)

    if mejor_vecino:
        Sv, m, mejora = mejor_vecino
        freq[m] += 1
        delta_acumulado[m] += mejora
        DicTabu[m] = IT_TABU
        return Sv
    else:
        return S
    
# ---------- Tabu Search ----------

def tabu_search(I, W, incompatibles, MAX):
    iter_actual = 0
    S = generar_estado_inicial(I, incompatibles)
    Sm = set(S)
    C = suma_de_montos(S, W)

    DicTabu = {}
    freq = defaultdict(int)
    delta_acumulado = defaultdict(float)

    print("Estado inicial:", S, "→", C)
    
    while iter_actual < MAX:
        Sv = buscar_mejor_vecino(S, Sm, I, W, incompatibles, DicTabu, freq, delta_acumulado)
        print("Vecino generado:",Sv)
        Cv = suma_de_montos(Sv, W)

        if Cv > C and es_factible(Sv, incompatibles):
            Sm = set(Sv)
            C = Cv
        S = Sv
        
        print("Movimientos TABU:",DicTabu)
        # Verifico si tengo que anular la prohibicion de algun movimiento tabu
        movs_a_borrar = []
        for m in DicTabu:
            DicTabu[m] -= 1
            if DicTabu[m] <= 0:
                movs_a_borrar.append(m)
        for m in movs_a_borrar:
            del DicTabu[m]


        # Trazado
        print(f"Iteración {iter_actual + 1}:")
        print(f"  - Estado actual S: {S} → {suma_de_montos(S, W)}")
        print(f"  - Mejor estado Sm: {Sm} → {suma_de_montos(Sm, W)}\n")

        iter_actual += 1

    return Sm

# ---------- Main ----------

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python ts.py inversores<i>.txt montos<i>.txt incompatibles<i>.txt")
        sys.exit(1)

    archivo_inversores = sys.argv[1]
    archivo_montos = sys.argv[2]
    archivo_incompatibles = sys.argv[3]

    I = leer_inversores(archivo_inversores)
    W = leer_montos(archivo_montos)
    incompatibles = leer_incompatibles(archivo_incompatibles)

    for i in range(1,6):
        resultado_estado_inicial= tabu_search(I, W, incompatibles, MAX_ITERACIONES)
        print(f"Mejor conjunto compatible {i}:",  resultado_estado_inicial)
        print(f"Monto total {i}:", suma_de_montos( resultado_estado_inicial, W))
        if i < 5:
            print("--------------------------------------------------------------")
            print("------------- -------Siguiente ejecucion ---------------------")
            print("--------------------------------------------------------------")

