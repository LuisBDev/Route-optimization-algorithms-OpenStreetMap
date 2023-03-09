import sys
import os
import random
import difflib
from pathlib import Path
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


class algoritmoBusqueda():

    def quickselect(self, list, left_idx, right_idx, kth_smallest):
        if left_idx == right_idx:
            return list[left_idx]

        pivot_idx = random.randint(left_idx, right_idx)

        pivot = list[pivot_idx]

        list[pivot_idx], list[right_idx] = list[right_idx], list[pivot_idx]

        store_idx = left_idx

        for i in range(left_idx, right_idx):
            if list[i] < pivot:
                list[store_idx], list[i] = list[i], list[store_idx]
                store_idx += 1

        list[right_idx], list[store_idx] = list[store_idx], list[right_idx]

        if kth_smallest == store_idx:
            return pivot
        elif kth_smallest < store_idx:
            return self.quickselect(list, left_idx, store_idx - 1, kth_smallest)
        else:
            return self.quickselect(list, store_idx + 1, right_idx, kth_smallest)

    def buscar_carpeta(self, nombre_busqueda, path):
        similitudes = []
        for carpeta in os.listdir(path):
            if carpeta == nombre_busqueda:
                return path, 100

        for nombre_carpeta in os.listdir(path):
            similitud = difflib.SequenceMatcher(None, nombre_busqueda, nombre_carpeta).ratio()
            if similitud >= 0.7:
                similitudes.append(similitud)

        if len(similitudes) > 0:
            algoritmo = algoritmoBusqueda()
            k = int(algoritmo.quickselect(similitudes, 0, len(similitudes)-1, len(similitudes)-1) * len(similitudes))
            carpeta_max_similitud = [nombre for nombre in os.listdir(path) if difflib.SequenceMatcher(None, nombre_busqueda, nombre).ratio() >= 0.7][k]
            ruta_carpeta = os.path.join(path, carpeta_max_similitud)

            return ruta_carpeta, similitudes[k]*100
        else:
            print("No se encontró ninguna carpeta que coincida con la búsqueda.")
            return None, 0


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
                    print(f"\nSugerencia N°{len(suggestions)}: --> {formatted}")
            if len(suggestions) == 0:
                print("\nLo siento, no se encontraron sugerencias para esa ubicación. Inténtalo de nuevo.")
                location = input("\nIntroduce una ubicación para buscar sugerencias -> ")
            else:
                flag = True

        selected = int(input("\nSelecciona el número de sugerencia que deseas usar -> "))
        while selected > len(suggestions) or selected < 1:
            print("\nSelecciona un número de sugerencia válido.")
            selected = int( input("\nSelecciona el número de sugerencia que deseas usar -> "))

        latitude = myjson["features"][selected -1]["geometry"]["coordinates"][1]
        longitude = myjson["features"][selected -1]["geometry"]["coordinates"][0]
        coordinates = [latitude, longitude]
        print(f"\nHas seleccionado la sugerencia {selected} para el nodo.")
        return suggestions[selected - 1], coordinates
        #Big O Notation:O(n^2)

    def area_especifica(self, area):
        sugerencias, coordenadas = self.search_suggestions(area)
        print(f"\n\tHas seleccionado el area especifica: {sugerencias}.\n")
        return area, coordenadas
        #Big O Notation: O(n)
    def busqueda_sugerencias(self, area):
        location, coordinates = self.search_suggestions(area)
        suggestions = [location]
        return suggestions[0], coordinates
        #Big O Notation: O(n)


class drawFolium():
    @staticmethod
    def save_map(nombre_inicio, nombre_destino, coordenadas_area, coordenadas_inicio, coordenadas_destino, area_especifica, medio):
       
        G = ox.graph_from_point(coordenadas_area, dist=5000, simplify=True, network_type=medio)
        punto_origen = (coordenadas_inicio[0], coordenadas_inicio[1])
        punto_destino = (coordenadas_destino[0], coordenadas_destino[1])

        # nearest_nodes recibe en orden longitud,latitud
        nodo_origen = ox.distance.nearest_nodes(G, punto_origen[1], punto_origen[0])
        nodo_destino = ox.distance.nearest_nodes(G, punto_destino[1], punto_destino[0])
        rutaFolium = ox.distance.shortest_path(G, nodo_origen, nodo_destino)

        mapaFolium = ox.plot_route_folium(G, rutaFolium, popup_attribute='length', tiles="OpenStreetMap", color='red')

        #Agregamos los marcadores y los nombres respectivos de las ubicaciones
        geolocator = Nominatim(user_agent="my-app")
        location_origen = geolocator.reverse(punto_origen)
        location_destino = geolocator.reverse(punto_destino)
        folium.Marker(location=punto_origen, icon=folium.Icon(color='green', icon='home'), popup=location_origen.address).add_to(mapaFolium)
        folium.Marker(location=punto_destino, icon=folium.Icon(color='blue', icon='flag'), popup=location_destino.address).add_to(mapaFolium)

        #Verificamos si existe una carpeta previamente con similitud
        path = Path(__file__).resolve().parent
        algoritmo = algoritmoBusqueda()
        global ruta_carpeta, ruta_archivo
        nombre_archivo = f"{nombre_inicio} - {nombre_destino}.html"
        ruta_carpeta, porcentaje_similitud = algoritmo.buscar_carpeta(area_especifica, path)

        if (porcentaje_similitud == 100):
            ruta_archivo = f"{path}/{area_especifica}/{nombre_archivo}"
            mapaFolium.save(ruta_archivo)

        elif porcentaje_similitud < 70 or ruta_carpeta is None:
            ruta_archivo = os.path.join(f"{path}/{area_especifica}", nombre_archivo)
            os.makedirs(area_especifica)
            mapaFolium.save(ruta_archivo)

        else:
            ruta_archivo = f"{ruta_carpeta}/{nombre_archivo}"
            mapaFolium.save(ruta_archivo)
       

    def display_pyqt():
        app = QApplication(sys.argv)
        window = QWidget()
        window.setWindowTitle('Trayecto mínimo - Implementación Dijkstra Algorithm - Grupo 4 ADA')
        view = QWebEngineView()

        with open(ruta_archivo, 'r') as f:
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
        #Big O Notation: O(1)

def search_api(lugar):

    url = (f"https://api.geoapify.com/v1/geocode/autocomplete?text={lugar}&apiKey=2e9ba25ff3ca47d0b02d81540edbafdd")
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    myjson = resp.json()

    return myjson
    #Big O Notation: O(1)

def final_menu():
    from MAIN_Proyecto_ADA import menu_implementacion
    os.system("cls")
    menu_implementacion
    #Big O Notation: O(1)s