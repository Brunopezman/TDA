import sys
import bisect

def contar_pilas(archivo_cartas):
    with open(archivo_cartas, "r") as file:
        cartas = [int(line.strip()) for line in file.readlines()]

    pilas = []  # Guarda el "techo" de cada pila

    for carta in cartas:
        pos = bisect.bisect_left(pilas, carta)  # Se busca dónde podríamos apilar esta carta

        if pos < len(pilas):  
            pilas[pos] = carta  # Reemplazamos el "techo" de la pila
        else:
            pilas.append(carta)  # Si no hay pila posible, creamos una nueva

    print(len(pilas))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.txt")
        sys.exit(1)

    contar_pilas(sys.argv[1])