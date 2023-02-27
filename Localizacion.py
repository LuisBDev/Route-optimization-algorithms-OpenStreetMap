import sys
import os
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pyproj import CRS
import contextily as ctx
import warnings
from shapely.geometry import LineString, Point
import folium
import requests
from requests.structures import CaseInsensitiveDict
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)


class Localizar():
    def area_especifica(area):

        sugerencias = []
        contador = 0
        # print(myjson) Imprimir contenido del json, features, properties, coordinates
        while (len(sugerencias) == 0):

            if (len(sugerencias) == 0 and contador > 0):
                area = input("\n\tIntroducir un area_especifica --> ")

            myjson = search_api(area)
            for i in range(len(myjson["features"])):
                if (myjson["features"][i]["properties"]["country"] == "Peru"):
                    address_line1 = myjson["features"][i]["properties"]["address_line1"]
                    formatted = myjson["features"][i]["properties"]["formatted"]
                    print(f"\nSugerencia N°{i+1}: --> {formatted}")
                    sugerencias.append(address_line1)

            contador = contador + 1

        seleccionFinal = int(input("\n\tSeleccionar N° de Sugerencia -> : "))

        while (seleccionFinal > len(sugerencias) or seleccionFinal < 0):
            print("\n\tSeleccione un valor correcto..")
            seleccionFinal = int(
                input("\n\tSeleccionar N° de Sugerencia -> : "))

        latitud = myjson["features"][seleccionFinal -
                                     1]["geometry"]["coordinates"][1]
        longitud = myjson["features"][seleccionFinal -
                                      1]["geometry"]["coordinates"][0]
        coordenadas = [latitud, longitud]

        print(
            f"\n\tHas seleccionado la sugerencia {seleccionFinal} para el area especifica.\n")

        return area, coordenadas

    def busqueda_sugerencias(lugar):
        sugerencias = []

        # print(myjson) Imprimir contenido del json, features, properties, coordinates
        contador = 0
        while (len(sugerencias) == 0):

            if (len(sugerencias) == 0 and contador > 0):
                lugar = input("\n\tIntroducir un area_especifica --> ")

            myjson = search_api(lugar)

            for i in range(len(myjson["features"])):
                if (myjson["features"][i]["properties"]["country"] == "Peru"):
                    address_line1 = myjson["features"][i]["properties"]["address_line1"]
                    formatted = myjson["features"][i]["properties"]["formatted"]
                    print(f"\nSugerencia N°{i+1}: --> {formatted}")
                    sugerencias.append(address_line1)

            contador = contador + 1

        seleccionFinal = int(input("\n\tSeleccionar N° de Sugerencia -> : "))

        while (seleccionFinal > len(sugerencias) or seleccionFinal < 0):
            print("\nSeleccione un valor correcto..")
            seleccionFinal = int(input("\nSeleccionar N° de Sugerencia -> : "))

        latitud = myjson["features"][seleccionFinal -
                                     1]["geometry"]["coordinates"][1]
        longitud = myjson["features"][seleccionFinal -
                                      1]["geometry"]["coordinates"][0]
        coordenadas = [latitud, longitud]

        print(
            f"\n\tHas seleccionado la sugerencia {seleccionFinal} para el nodo.\n")

        return sugerencias[seleccionFinal-1], coordenadas


class drawFolium():
    def save_map(coordenadas_area, coordenadas_inicio, coordenadas_destino, area_especifica, medio, nodo_inicio, nodo_destino_para):
        G = ox.graph_from_point(
            coordenadas_area, dist=5000, simplify=True, network_type=medio)
        punto_origen = (coordenadas_inicio[0], coordenadas_inicio[1])
        punto_destino = (coordenadas_destino[0], coordenadas_destino[1])

        # nearest_nodes recibe en orden longitud,latitud
        nodo_origen = ox.distance.nearest_nodes(
            G, punto_origen[1], punto_origen[0])
        nodo_destino = ox.distance.nearest_nodes(
            G, punto_destino[1], punto_destino[0])
        rutaFolium = ox.distance.shortest_path(G, nodo_origen, nodo_destino)

        mapaFolium = ox.plot_route_folium(
            G, rutaFolium, popup_attribute='length', tiles="OpenStreetMap", color='red')

        folium.Marker(location=punto_origen, icon=None).add_to(mapaFolium)
        folium.Marker(location=punto_destino, icon=None).add_to(mapaFolium)

        '''if not os.path.exists(area_especifica):
            os.makedirs(area_especifica)'''

        mapaFolium.save(f"{area_especifica}.html")
        ''' global area_esp, ini, des
        area_esp = area_especifica
        ini, des = nodo_inicio, nodo_destino_para'''

    def display_pyqt(area_especifica, nodo_inicio, nodo_destino):
        app = QApplication(sys.argv)
        window = QWidget()
        window.setWindowTitle(
            'Trayecto mínimo - Implementación Dijkstra Algorithm - Grupo 4 ADA')
        view = QWebEngineView()

        with open(f'{area_especifica}/{nodo_inicio}-{nodo_destino}.html', 'r') as f:
            html = f.read()

        view.setHtml(html)
        view.setFixedSize(1340, 760)
        layout = QVBoxLayout(window)
        layout.addWidget(view)
        layout.setAlignment(view, Qt.AlignCenter)

        window.show()

        try:
            sys.exit(app.exec_())
        except SystemExit:
            print('Cerrando Folium...')
        finally:
            final_menu()


def search_api(lugar):

    url = (
        f"https://api.geoapify.com/v1/geocode/autocomplete?text={lugar}&apiKey=2e9ba25ff3ca47d0b02d81540edbafdd")
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    myjson = resp.json()

    return myjson


def final_menu():
    from MAIN_Proyecto_ADA import menu_implementacion
    os.system("cls")
    menu_implementacion
