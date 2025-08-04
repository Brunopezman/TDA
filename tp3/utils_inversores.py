import random

# constantes para tipo de movimiento
AGREGAR = "agregar"
QUITAR = "quitar"
INTERCAMBIAR = "intercambiar"

# ---------- Funciones auxiliares ----------
def leer_inversores(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def leer_montos(path):
    W = {}
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                partes = line.strip().split()
                W[partes[0]] = int(partes[1])
    return W

def leer_incompatibles(path):
    incompatibles = {}
    with open(path, 'r') as f:
        for line in f:
            partes = line.strip().split(":")
            inversor = partes[0].strip()
            if partes[1] is not None:
                incompatibles[inversor] = set(partes[1].split(","))
            else:
                incompatibles[inversor] = set()
    return incompatibles

def es_factible(S, incompatibles):
    for i in S:
        for j in incompatibles.get(i, []):
            if j in S:
                return False
    return True

def suma_de_montos(S, W):
    return sum(W[i] for i in S)

def generar_estado_inicial(I, incompatibles):
    S = set()
    I_aleatorio = list(I)
    random.shuffle(I_aleatorio)
    
    for i in I_aleatorio:
        if es_factible(S | {i}, incompatibles):
            S.add(i)
    
    return S