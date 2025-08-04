import networkx as nx
from collections import deque, Counter
import sys

# -------------------------------------
# Camino aumentante (BFS)
# -------------------------------------
def encontrar_camino_aumentante(capacidades, flujo, s, t):
    padre = {s: None}
    cuello_botella = {s: float('inf')}
    queue = deque([s])

    while queue:
        u = queue.popleft()
        for v in capacidades.get(u, {}):
            capacidad_residual = capacidades[u][v] - flujo[u][v]
            if capacidad_residual > 0 and v not in padre:
                padre[v] = u
                cuello_botella[v] = min(cuello_botella[u], capacidad_residual)
                if v == t:
                    camino = []
                    nodo = t
                    while nodo != s:
                        camino.append(nodo)
                        nodo = padre[nodo]
                    camino.append(s)
                    camino.reverse()
                    return camino, cuello_botella[t]
                queue.append(v)
    return None, 0

# -------------------------------------
# Ford-Fulkerson (BFS => Edmonds-Karp)
# -------------------------------------
def ford_fulkerson(G, s, t):
    flujo = {u: {} for u in G}
    for u in G:
        for v in G[u]:
            flujo[u][v] = 0
            if v not in flujo:
                flujo[v] = {}
            flujo[v][u] = 0

    capacidades = {u: {} for u in G}
    for u in G:
        for v in G[u]:
            capacidades[u][v] = G[u][v]['capacity']
            if v not in capacidades:
                capacidades[v] = {}
            if u not in capacidades[v]:
                capacidades[v][u] = 0 

    max_flujo = 0

    while True:
        camino, cuello = encontrar_camino_aumentante(capacidades, flujo, s, t)
        if not camino:
            break
        for i in range(len(camino) - 1):
            u = camino[i]
            v = camino[i + 1]
            flujo[u][v] += cuello
            flujo[v][u] -= cuello
        max_flujo += cuello

    return max_flujo, flujo

# -------------------------------------
# Construcción del grafo de flujo
# -------------------------------------
def armado_red_de_flujo(n, s, ciudades_file, espias_file):
    G = nx.DiGraph()
    fuente = "F"
    sumidero = "T"
    G.add_node(fuente)
    G.add_node(sumidero)

    vuelos = []
    ciudades = set()
    with open(ciudades_file, "r") as f:
        for linea in f:
            origen, destino = linea.strip().split(",")
            vuelos.append((origen, destino))
            ciudades.update([origen, destino])


    espias = []
    centros = []
    with open(espias_file, "r") as f:
        for i, linea in enumerate(f):
            _, ciudad = linea.strip().split(",")
            if i < n:
                espias.append(ciudad)
            else:
                centros.append(ciudad)

    for ciudad in ciudades:
        G.add_node(f"{ciudad}_in")
        G.add_node(f"{ciudad}_out")
        G.add_edge(f"{ciudad}_in", f"{ciudad}_out", capacity=s)

    for origen, destino in vuelos:
        G.add_edge(f"{origen}_out", f"{destino}_in", capacity=float('inf'))
        G.add_edge(f"{destino}_out", f"{origen}_in", capacity=float('inf'))

    for ciudad in espias:
        nodo = f"{ciudad}_in"
        if G.has_edge(fuente, nodo):
            G[fuente][nodo]["capacity"] += 1
        else:
            G.add_edge(fuente, nodo, capacity=1)

    for ciudad in centros:
        nodo = f"{ciudad}_out"
        if G.has_edge(nodo, sumidero):
            G[nodo][sumidero]["capacity"] += 1
        else:
            G.add_edge(nodo, sumidero, capacity=1)

    return G, fuente, sumidero

# -------------------------------------
# Armado de rutas individuales
# -------------------------------------
def armado_de_ruta(G, flujo, fuente, sumidero):
    rutas = []
    flujo_copia = {u: flujo[u].copy() for u in flujo}

    for vecino in G[fuente]:
        while flujo_copia[fuente].get(vecino, 0) > 0:
            ciudades_ruta = []
            actual = vecino
            flujo_copia[fuente][vecino] -= 1
            prev_ciudad = None

            while actual != sumidero:
                if actual in {fuente, sumidero}:
                    ciudad = None
                elif actual.endswith("_in") or actual.endswith("_out"):
                    ciudad = actual.split("_")[0]
                else:
                    ciudad = actual

                if ciudad and ciudad != prev_ciudad:
                    ciudades_ruta.append(ciudad)
                    prev_ciudad = ciudad

                for siguiente in G[actual]:
                    if flujo_copia[actual].get(siguiente, 0) > 0:
                        flujo_copia[actual][siguiente] -= 1
                        actual = siguiente
                        break
                else:
                    break  # Evita loop infinito si no hay siguiente

            rutas.append(ciudades_ruta)

    return rutas

# -------------------------------------
# Lógica principal
# -------------------------------------
def traslado(n, s, ciudades_file, espias_file):
    G, fuente, sumidero = armado_red_de_flujo(n, s, ciudades_file, espias_file)
    flujo_max, flujo = ford_fulkerson(G, fuente, sumidero)

    if flujo_max != n:
        print("Es imposible lograr el objetivo")
        return

    rutas = armado_de_ruta(G, flujo, fuente, sumidero)
    for i, camino in enumerate(rutas):
        print(f"Espia {i + 1},{','.join(camino)}")

# -------------------------------------
# Main
# -------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3 traslado.py <n> <s> ciudades.txt espias.txt")
        sys.exit(1)

    n = int(sys.argv[1])
    s = int(sys.argv[2])
    ciudades_file = sys.argv[3]
    espias_file = sys.argv[4]
    traslado(n, s, ciudades_file, espias_file)
