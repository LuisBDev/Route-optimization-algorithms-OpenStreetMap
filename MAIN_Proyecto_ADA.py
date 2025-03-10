import os
import time
import matplotlib.pyplot as plt
import warnings
from Localizacion import *
from DijkstraMain import *
from SeleccionRuta import *


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)


def input_nodo():

    print("\n##### [BÚSQUEDA DE NODO.] #####\n\t ")
    nodo_nombre = input("\tIntroducir nodo --> ")
    localizar = Localizar()
    nodo_nombre, coordenadas_nodo = localizar.busqueda_sugerencias(nodo_nombre)
    print(f"Nodo: {nodo_nombre} - Coordenadas: {coordenadas_nodo}")
    return nodo_nombre, coordenadas_nodo
    #Big O Notation: O(1)



def obtener_area_especifica():

    print("\n##### [BÚSQUEDA ÁREA ESPECÍFICA.] #####")
    area = input("\n\tIntroducir area_especifica --> ")
    localizar = Localizar()
    area_especifica, coordenadas_area = localizar.area_especifica(area)
    print(f"Coordenadas area_especifica: {coordenadas_area[0],coordenadas_area[1]}")

    return area_especifica, coordenadas_area
    #Big O Notation: O(1)



def medio_de_transporte():
    medio = int(input("\nSeleccion de Medio de Transporte\n\t1. Walk.\n\t2. Drive.\n\t3. Bike.\n\t0. Salir\n\n\t--> "))
    if (medio == 0):
        return
    elif (medio == 1):
        return "walk"
    elif (medio == 2):
        return "drive"
    elif (medio == 3):
        return "bike"
    else:
        print("Opción inválida...")
        return medio_de_transporte()
    #Big O Notation: O(1)
    


def menu_opciones(coordenadas_inicio, area_especifica, opcion=None):
    if opcion is None:
        opcion = int(input("\n\n\t1. Display folium.\n\t0. Salir\n\n\t--> "))
        while (opcion not in [0, 1]):
            print("Opción inválida...")
            opcion = int(input("\n\n\t1. Display folium.\n\t0. Salir\n\n\t--> "))
    if opcion == 0:
        return
    elif opcion == 1:
        drawFolium.display_pyqt()

    menu_opciones(coordenadas_inicio, area_especifica)
    #Big O-Notation: O(n)


def menu_implementacion():

    area_especifica, coordenadas_area = obtener_area_especifica()
    nodo_inicio, coordenadas_inicio = input_nodo()
    nodo_destino, coordenadas_destino = input_nodo()
    medio_transporte = medio_de_transporte()
    
    execution_time = drawFolium.save_map(nodo_inicio, nodo_destino, coordenadas_area, coordenadas_inicio,coordenadas_destino, area_especifica, medio_transporte)
    
    print(f"Tiempo de ejecución: {execution_time} ms")
    menu_opciones(coordenadas_inicio, area_especifica)

    #Big O Notation: O(1)

def menu_algoritmos(opcion=None):
    opciones = {
        1: display_dijkstra.main,
        2: menu_implementacion,
        3: main
    }
    if opcion == 0:
        return
        
    if opcion in opciones:
        opciones[opcion]()
        os.system("cls")
    
    new_opcion = int(input("\nSeleccionar el grafo a implementar:\n\n\t1. Dijkstra CodeBase\n\t""2. Implementacion Vial\n\t3. Mejor ruta - Algoritmo Voraz\n\t0. Salir de la aplicacion.\n\n\t\t---> "))
    menu_algoritmos(new_opcion)
    #Big O Notation: O(n)


menu_algoritmos()