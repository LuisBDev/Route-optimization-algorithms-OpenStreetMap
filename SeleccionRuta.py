import matplotlib.pyplot as plt
import networkx as nx

class SeleccionRuta:
    def __init__(self):
        self.nodos = set()
        self.aristas = dict()
        self.distancias = dict()

    def agregar_nodo(self, valor):
        self.nodos.add(valor)

    def agregar_arista(self, desde, hasta, distancia):
        self.aristas.setdefault(desde, [])
        self.aristas[desde].append(hasta)
        self.distancias[(desde, hasta)] = distancia

    def voraz(self, origen, destino, distancia_maxima):
        ruta = [origen]
        distancia_recorrida = 0
        nodo_actual = origen

        while nodo_actual != destino and distancia_recorrida <= distancia_maxima:
            vecinos = self.aristas[nodo_actual]
            distancias = [self.distancias[(nodo_actual, vecino)] for vecino in vecinos]
            mejor_vecino = vecinos[distancias.index(min(distancias))]
            distancia_recorrida += min(distancias)

            if distancia_recorrida <= distancia_maxima:
                ruta.append(mejor_vecino)
                nodo_actual = mejor_vecino
            else:
                break

        if nodo_actual == destino and distancia_recorrida <= distancia_maxima:
            return ruta
        else:
            return None

    def dibujar(self, ruta):
        G = nx.Graph()

        for nodo in self.nodos:
            G.add_node(nodo)

        for arista, distancia in self.distancias.items():
            G.add_edge(arista[0], arista[1], weight=distancia)

        pos = nx.spring_layout(G)
        nodos_rojos = ruta
        nodos_celestes = list(self.nodos - set(ruta))

        nx.draw_networkx_nodes(G, pos, nodelist=nodos_rojos, node_color='r')
        nx.draw_networkx_nodes(G, pos, nodelist=nodos_celestes, node_color='c')
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)

        edge_labels = {(arista[0], arista[1]): str(distancia) for arista, distancia in self.distancias.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()

def main():
    g = SeleccionRuta()

    origen = input("Ingrese el lugar de origen: ")
    destino = input("Ingrese el lugar de destino: ")
    distancia_maxima = int(input("Ingrese la distancia máxima permitida: "))
    numero_aristas = int(input("Ingrese el número de rutas que desea agregar: "))

    for i in range(numero_aristas):
        desde = input(f"Ingrese el lugar de origen de la arista {i+1}: ")
        hasta = input(f"Ingrese el lugar de destino de la arista {i+1}: ")
        distancia = int(input(f"Ingrese la distancia entre los lugares {desde} y {hasta}: "))
        g.agregar_nodo(desde)
        g.agregar_nodo(hasta)
        g.agregar_arista(desde, hasta, distancia)
    ruta = g.voraz(origen, destino, distancia_maxima)

    if ruta is None:
        print("No se pudo encontrar una ruta que cumpla con las restricciones.")
    else:
        print(f"La ruta encontrada es: {ruta}")
        g.dibujar(ruta)


