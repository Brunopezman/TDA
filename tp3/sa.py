import random
import math
import sys
from utils_inversores import *

TEMP_INICIAL = 100
FACTOR_ENFRIAMIENTO = 0.95
MAX_ITERACIONES = 10

def generar_vecino(S, I, incompatibles):
    while True:
        S_prime = set(S)
        op = random.choice([AGREGAR, QUITAR, INTERCAMBIAR])
        
        if op == AGREGAR:
            posibles = list(set(I) - S)
            if posibles:
                i = random.choice(posibles)
                S_prime.add(i)

        elif op == QUITAR:
            if S:
                i = random.choice(list(S))
                S_prime.remove(i)

        elif op == INTERCAMBIAR:
            if S and set(I) - S:
                i = random.choice(list(S))
                j = random.choice(list(set(I) - S))
                S_prime.remove(i)
                S_prime.add(j)

        if es_factible(S_prime, incompatibles):
            return S_prime

def determinar_el_siguiente_estado_actual(T, S, Sv, W):
    C = suma_de_montos(S, W)
    Cv = suma_de_montos(Sv, W)

    if Cv > C:
        return Sv
    
    R = random.random()
    exp = (Cv - C) / T

    if R < math.exp(exp):
        return Sv

    return S

# ---------- Algoritmo principal ----------

def simulated_annealing(I, W, incompatibles, C, MAX, T0):
    IT = 0
    S0 = generar_estado_inicial(I, incompatibles)
    S = set(S0)
    Sm = set(S0)
    T = T0

    print("Estado inicial:", S0, "→", suma_de_montos(S0, W))

    while IT < MAX:
        Sv = generar_vecino(S, I, incompatibles)
        print('Vecino generado:',Sv)
        S = determinar_el_siguiente_estado_actual(T, S, Sv, W)
        if suma_de_montos(S, W) > suma_de_montos(Sm, W):
            Sm = set(S)

        # Trazado por consola
        print(f"Iteración {IT + 1}:")
        print(f"  - Estado actual S: {S} → {suma_de_montos(S, W)}")
        print(f"  - Mejor estado Sm: {Sm} → {suma_de_montos(Sm, W)}")
        print(f"  - Temperatura T: {T:.4f}\n")

        T *= C
        IT += 1

    return Sm

# ---------- Main ----------

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python sa.py inversores<i>.txt montos<i>.txt incompatibles<i>.txt")
        sys.exit(1)
    
    archivo_inversores = sys.argv[1]
    archivo_montos = sys.argv[2]
    archivo_incompatibles = sys.argv[3]
     
    inversores = leer_inversores(archivo_inversores)
    montos = leer_montos(archivo_montos)
    incompatibles = leer_incompatibles(archivo_incompatibles)

    for i in range(1,6):
        resultado = simulated_annealing(
            inversores, montos, incompatibles,
            FACTOR_ENFRIAMIENTO, MAX_ITERACIONES, TEMP_INICIAL
        )
        print(f"Mejor conjunto compatible {i}:", resultado)
        print(f"Monto total {i}:", suma_de_montos(resultado, montos))
        if i < 5:
            print("--------------------------------------------------------------")
            print("------------- -------Siguiente ejecucion ---------------------")
            print("--------------------------------------------------------------")