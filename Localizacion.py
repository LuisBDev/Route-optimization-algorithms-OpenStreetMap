import json
import sys
import os
import osmnx as ox
import warnings
import folium
import requests
from requests.structures import CaseInsensitiveDict
import sys
from geopy.geocoders import Nominatim
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)


class Localizar():

    def search_suggestions(self, location, flag=False):
        suggestions = []
        while not flag:

            myjson = search_api(location)
            for i in range(len(myjson["features"])):
                if myjson["features"][i]["properties"]["country"] == "Peru":
                    address_line1 = myjson["features"][i]["properties"]["address_line1"]
                    formatted = myjson["features"][i]["properties"]["formatted"]
                    suggestions.append(address_line1)
                    print(
                        f"\nSugerencia N°{len(suggestions)}: --> {formatted}")
            if len(suggestions) == 0:
                print(
                    "\nLo siento, no se encontraron sugerencias para esa ubicación. Inténtalo de nuevo.")
                location = input(
                    "\nIntroduce una ubicación para buscar sugerencias -> ")
            else:
                flag = True

        selected = int(
            input("\nSelecciona el número de sugerencia que deseas usar -> "))
        while selected > len(suggestions) or selected < 1:
            print("\nSelecciona un número de sugerencia válido.")
            selected = int(
                input("\nSelecciona el número de sugerencia que deseas usar -> "))

        latitude = myjson["features"][selected -
                                      1]["geometry"]["coordinates"][1]
        longitude = myjson["features"][selected -
                                       1]["geometry"]["coordinates"][0]
        coordinates = [latitude, longitude]
        print(
            f"\nHas seleccionado la sugerencia {selected} para el nodo.")
        return suggestions[selected - 1], coordinates

    def area_especifica(self, area):
        sugerencias, coordenadas = self.search_suggestions(area, flag=False)
        print(f"\n\tHas seleccionado el area especifica: {sugerencias}.\n")
        return area, coordenadas

    def busqueda_sugerencias(self, area):
        location, coordinates = self.search_suggestions(area, flag=False)
        suggestions = [location]
        return suggestions[0], coordinates


class drawFolium():
    @staticmethod
    def save_map(coordenadas_area, coordenadas_inicio, coordenadas_destino, area_especifica, medio):
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

        # add markers for starting and ending points
        geolocator = Nominatim(user_agent="my-app")
        location_origen = geolocator.reverse(punto_origen)
        location_destino = geolocator.reverse(punto_destino)
        folium.Marker(location=punto_origen, icon=folium.Icon(
            color='green', icon='home'), popup=location_origen.address).add_to(mapaFolium)
        folium.Marker(location=punto_destino, icon=folium.Icon(
            color='blue', icon='flag'), popup=location_destino.address).add_to(mapaFolium)

        # get the address of the starting and ending points
        # add markers for starting and ending points with popups showing the address

        '''if not os.path.exists(area_especifica):
            os.makedirs(area_especifica)'''

        # implementar funcion de comparacion de nombres de archivos
        mapaFolium.save(f"{area_especifica}.html")
        ''' global area_esp, ini, des
        area_esp = area_especifica
        ini, des = nodo_inicio, nodo_destino_para'''

    def display_pyqt(area_especifica):
        app = QApplication(sys.argv)
        window = QWidget()
        window.setWindowTitle(
            'Trayecto mínimo - Implementación Dijkstra Algorithm - Grupo 4 ADA')
        view = QWebEngineView()

        with open(f'{area_especifica}.html', 'r') as f:
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
