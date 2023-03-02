import matplotlib.pyplot as plt
from Ruta import *


class SeleccionadorRutas:
    def __init__(self, distancia_maxima):
        self.distancia_maxima = distancia_maxima
        self.rutas = []

    def agregar_ruta(self, distancia, tiempo):
        self.rutas.append(Ruta(distancia, tiempo))

    def seleccionar_rutas_voraz(self):
        rutas_ordenadas = sorted(
            self.rutas, key=lambda ruta: ruta.distancia, reverse=True)
        distancia_total = 0
        tiempo_total = 0
        rutas_seleccionadas = []
        for ruta in rutas_ordenadas:
            if distancia_total + ruta.distancia <= self.distancia_maxima:
                rutas_seleccionadas.append(ruta)
                distancia_total += ruta.distancia
                tiempo_total += ruta.tiempo
        return rutas_seleccionadas, tiempo_total


class ruta_selec():
    def main(self):
        num_rutas = int(input("Ingrese la cantidad de rutas: "))
        distancia_maxima = int(
            input("Ingrese la distancia máxima permitida: "))
        seleccionador = SeleccionadorRutas(distancia_maxima=distancia_maxima)
        for i in range(num_rutas):
            print(f"Ingrese los datos de la ruta {i + 1}")
            distancia = int(input("Distancia de la ruta: "))
            tiempo = int(input("Tiempo de la ruta: "))
            seleccionador.agregar_ruta(distancia, tiempo)
        rutas_seleccionadas, tiempo_total = seleccionador.seleccionar_rutas_voraz()
        distancias = []
        tiempos = []
        print("Rutas seleccionadas:")
        for ruta in rutas_seleccionadas:
            distancias.append(ruta.distancia)
            tiempos.append(ruta.tiempo)
            print(f"- Ruta de distancia {ruta.distancia} y tiempo {ruta.tiempo}")
        distancias, tiempos = zip(*sorted(zip(distancias, tiempos), key=lambda x: x[1]))
        fig, ax = plt.subplots()
        ax.plot(distancias, tiempos, 'o-')
        ax.set_xlabel('Distancia de la ruta')
        ax.set_ylabel('Tiempo de la ruta')
        ax.set_title('Rutas seleccionadas')
        plt.show()
        print(f"Tiempo total: {tiempo_total}")
