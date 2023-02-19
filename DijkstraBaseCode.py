import networkx as nx
import matplotlib.pyplot as plt


class Vertice:

    def __init__(self, id):
        self.id = id
        self.visitado = False
        self.distancia = float('inf')
        self.padre = None
        self.vecinos = []

    def agregar_vecinos(self, v, p):
        if v not in self.vecinos:
            self.vecinos.append([v, p])


class Grafo:

    def __init__(self):
        self.grafica = nx.Graph()
        self.vertice = {}

    def mostrar_grafica(self):
        pos = nx.layout.spring_layout(self.grafica)
        nx.draw_networkx(self.grafica, pos)
        labels = nx.get_edge_attributes(self.grafica, 'weight')
        nx.draw_networkx_edge_labels(self.grafica, pos, edge_labels=labels)
        plt.show()

    def agregar_vertice(self, v):
        if v not in self.vertice:
            self.vertice[v] = Vertice(v)

    def agregar_aristas(self, a, b, peso):
        if a in self.vertice and b in self.vertice:
            self.vertice[a].agregar_vecinos(b, peso)
            self.vertice[b].agregar_vecinos(a, peso)

            self.grafica.add_edge(a, b, weight=peso)

    def caminos(self, b):
        caminos = []
        actual = b
        while actual is not None:
            caminos.insert(0, actual)
            actual = self.vertice[actual].padre
        print('La ruta mas corta seria ', caminos, ' y la distancia es ', self.vertice[b].distancia)
        plt.title(f'El camino minimo es {caminos}')
        self.mostrar_grafica()

    def menor_peso(self, lista):
        if len(lista) > 0:
            menor = self.vertice[lista[0]].distancia
            v = lista[0]
            for e in lista:
                if menor > self.vertice[e].distancia:
                    menor = self.vertice[e].distancia
                    v = e
            return v

    def dijkstra(self, a):
        if a in self.vertice:
            self.vertice[a].distancia = 0
            inicial = a
            no_visitados = []
            for v in self.vertice:
                if v != inicial:
                    self.vertice[v].distancia = float('inf')
                self.vertice[v].padre = None
                no_visitados.append(v)
            while len(no_visitados) > 0:
                for vecino in self.vertice[inicial].vecinos:
                    if not self.vertice[vecino[0]].visitado:
                        if self.vertice[inicial].distancia + vecino[1] < self.vertice[vecino[0]].distancia:
                            self.vertice[vecino[0]].distancia = self.vertice[inicial].distancia + vecino[1]
                            self.vertice[vecino[0]].padre = inicial
                self.vertice[inicial].visitado = True
                no_visitados.remove(inicial)
                inicial = self.menor_peso(no_visitados)
        else:
            return False
        
