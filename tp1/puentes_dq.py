import sys

def leer_barrios(ruta):
    with open(ruta) as f:
        partes = f.read().strip().split("\n\n")
        norte = partes[0].splitlines()
        sur = partes[1].splitlines()

    orden_norte = {nombre: i for i, nombre in enumerate(norte)}
    orden_sur = {nombre: i for i, nombre in enumerate(sur)}

    return orden_norte, orden_sur

def leer_propuestas(ruta):
    with open(ruta) as f:
        propuestas = []
        for linea in f:
            norte, sur = linea.strip().split(",")
            propuestas.append((norte.strip().strip("."), sur.strip().strip(".")))
    return propuestas

def contar_inversiones(arr):
    def merge_sort(lista):
        if len(lista) <= 1:
            return lista, 0
        mid = len(lista) // 2
        izquierda, inv_izq = merge_sort(lista[:mid])
        derecha, inv_der = merge_sort(lista[mid:])
        merged, inv_merge = merge(izquierda, derecha)
        return merged, inv_izq + inv_der + inv_merge

    def merge(izq, der):
        resultado = []
        i = j = inv = 0
        while i < len(izq) and j < len(der):
            if izq[i] <= der[j]:
                resultado.append(izq[i])
                i += 1
            else:
                resultado.append(der[j])
                inv += len(izq) - i
                j += 1
        resultado += izq[i:]
        resultado += der[j:]

        return resultado, inv


    _, total = merge_sort(arr)
    return total

def main():
    archivo_barrios, archivo_propuestas = sys.argv[1] , sys.argv[2]


    dicc_norte, dicc_sur = leer_barrios(archivo_barrios)
    propuestas = leer_propuestas(archivo_propuestas)


    propuestas.sort(key=lambda x: dicc_norte[x[0]])
    lista_sur = [dicc_sur[sur] for _, sur in propuestas]

    cruces = contar_inversiones(lista_sur)
    print(cruces)

if __name__ == "__main__":
    main()