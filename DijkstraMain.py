import copy
from DijkstraBaseCode import *


def grafica():
    pass


def verificar(lista, a, b):
    if a and b in lista:
        return True
    else:
        print('ERROR!!! NO SE ENCONTRÓ LA CIUDAD')
        return False


def origen_destino(g):
    guardar = g
    print('------------------')
    print('Recorridos minimos')
    print('------------------')
    origen = input('Ingrese la ciudad de origen: ')
    destino = input('Ingrese la ciudad destino: ')
    guardar.dijkstra(origen)
    return print(guardar.caminos(destino))


class display_dijkstra():
    def main():
        g = Grafo()
        # Agregar ciudades
        print('¿Cuantas ciudades desea ingresar?')
        opc = int(input('--> '))
        Ciudades = []
        for i in range(0, opc):
            ciud = input(f'Ciudad {i + 1}: ')
            Ciudades.append(ciud)
        for i in Ciudades:
            g.agregar_vertice(i)

        # Agregar aristas y peso
        print('------------------------')
        print('Agregar aristas y pesos ')
        print('------------------------')

        sino = 'S'
        while sino == 'S' or sino == 's':
            veri = False
            while veri is False:
                ciudad1 = input('Ingrese la primera ciudad: ')
                ciudad2 = input('Ingrese la segunda ciudad: ')
                veri = verificar(Ciudades, ciudad1, ciudad2)

            distancia = int(
                input('Ingrese la distancia en kilometros entre las ciudades: '))
            g.agregar_aristas(ciudad1, ciudad2, distancia)

            sino = input('¿Desea continuar? (S/N) --> ')
            while sino not in ['S', 's', 'N', 'n']:
                sino = input("Introducir valor correcto: (S/N) --> ")
        g.mostrar_grafica()
        # Caminos minimos
        sino = 'S'
        while sino == 'S' or sino == 's':
            copia = copy.deepcopy(g)
            origen_destino(copia)
            sino = input('¿Desea ingresar otros datos? (S/N) --> ')
            while sino not in ['S', 's', 'N', 'n']:
                sino = input("Introducir valor correcto: (S/N) --> ")
