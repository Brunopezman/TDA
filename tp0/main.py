from collections import deque
import sys

def apilar_cartas(nombre_archivo):
    cantidad_pilas = []

    with open(nombre_archivo, 'r') as f:
        for linea in f:
            if linea.strip() == "":
                continue
            carta = int(linea.strip())

            colocada = False
            for p in cantidad_pilas:
                if carta < p[0]:
                    p.appendleft(carta)
                    colocada = True
                    break

            if not colocada:
                nueva_pila = deque([carta])
                cantidad_pilas.append(nueva_pila)

    return len(cantidad_pilas)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.txt")
        sys.exit(1)

    archivo = sys.argv[1]
    resultado = apilar_cartas(archivo)
    print(resultado)
