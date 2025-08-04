import sys

def leer_ofertas(path):
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        m = int(lines[0])
        nombres = []
        ofertas = []
        for line in lines[1:]:
            partes = line.split(',')
            nombres.append(partes[0])
            ofertas.append([int(x) for x in partes[1:]])
    return m, nombres, ofertas

def leer_enemigos(path):
    enemigos = {}
    with open(path, 'r') as f:
        for line in f:
            partes = line.strip().split(',')
            if len(partes) > 1:
                enemigos[partes[0]] = set(partes[1:])
            else:
                enemigos[partes[0]] = set()
    return enemigos

def adyacentes(j, m):
    return {(j - 1 + m) % m, (j + 1) % m}

def es_valida(asignacion, invitado_idx, porcion_idx, nombres, enemigos, m):
    invitado = nombres[invitado_idx]
    for p, idx in enumerate(asignacion):
        if idx is not None:
            otro = nombres[idx]
            if porcion_idx in adyacentes(p, m):
                if otro in enemigos.get(invitado, set()) or invitado in enemigos.get(otro, set()):
                    return False
    return True

def cota_superior(ganancia_actual, ofertas, asignacion, asignados, m):
    no_asignados = [i for i in range(len(ofertas)) if i not in asignados]
    porciones_restantes = [j for j, a in enumerate(asignacion) if a is None]
    mejores = [max((ofertas[i][j] for i in no_asignados), default=0) for j in porciones_restantes]
    return ganancia_actual + sum(mejores)

def branch_and_bound_dfs(m, nombres, ofertas, enemigos):
    global mejor_ganancia, mejor_asignacion
    stack = []

    asignacion_inicial = [None] * m
    asignados_inicial = set()
    ganancia_inicial = 0
    estimado = cota_superior(ganancia_inicial, ofertas, asignacion_inicial, asignados_inicial, m)
    stack.append((estimado, 0, asignacion_inicial, asignados_inicial, ganancia_inicial))

    while stack:
        # ordenar para que el mas prometedor este al final (LIFO)
        stack.sort(key=lambda x: x[0], reverse=True)
        _, k, asignacion, asignados, ganancia_actual = stack.pop()

        if k == m:
            if ganancia_actual > mejor_ganancia:
                mejor_ganancia = ganancia_actual
                mejor_asignacion = asignacion[:]
            continue

        for i in range(len(nombres)):
            if i not in asignados and es_valida(asignacion, i, k, nombres, enemigos, m):
                nueva_asignacion = asignacion[:]
                nueva_asignacion[k] = i
                nuevo_asignados = asignados.copy()
                nuevo_asignados.add(i)
                nueva_ganancia = ganancia_actual + ofertas[i][k]

                estimado = cota_superior(nueva_ganancia, ofertas, nueva_asignacion, nuevo_asignados, m)
                if estimado > mejor_ganancia:
                    stack.append((estimado, k + 1, nueva_asignacion, nuevo_asignados, nueva_ganancia))

        # considerar no asignar porcion
        nueva_asignacion = asignacion[:]
        nueva_asignacion[k] = None
        estimado = cota_superior(ganancia_actual, ofertas, nueva_asignacion, asignados, m)
        if estimado > mejor_ganancia:
            stack.append((estimado, k + 1, nueva_asignacion, asignados.copy(), ganancia_actual))

if __name__ == "__main__":
    archivo_ofertas = sys.argv[1]
    archivo_enemigos = sys.argv[2]

    m, nombres, ofertas = leer_ofertas(archivo_ofertas)
    enemigos = leer_enemigos(archivo_enemigos)

    mejor_ganancia = 0
    mejor_asignacion = []

    branch_and_bound_dfs(m, nombres, ofertas, enemigos)

    print(f"La ganancia máxima a obtener es: {mejor_ganancia}")
    ganadores = [nombres[i] if i is not None else "Nadie" for i in mejor_asignacion]
    print(f"Los invitados ganadores son: {', '.join(ganadores)}")
