import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()

    def getAllYears(self):
        return DAO.getAllYears()

    def getSquadreAnno(self, year):
        self._squadre = DAO.getSquadreAnno(year)
        return self._squadre

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._squadre)

        for v in self._squadre:
            for u in self._squadre:
                if v!=u and not self._grafo.has_edge(u, v):
                    peso=u.salary+v.salary
                    self._grafo.add_edge(v, u, weight=peso)
                    print(v, u, peso)

        print(self._grafo)


    def getDettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getVicini(self, squadra):
        result = []
        vicini = nx.neighbors(self._grafo, squadra)
        for v in vicini:
            result.append( (v, self._grafo[squadra][v]["weight"]) )
        result.sort(key=lambda x:x[1], reverse=True)

        return result


    def getPercorso(self, squadra):

        self._bestSol = []
        self._bestScore = 0

        parziale = [squadra]
        for node in nx.neighbors(self._grafo, squadra):
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()

        return self.toSoluzione(self._bestSol), self._bestScore


    def _ricorsione(self, parziale):

        if self._getScore(parziale) > self._bestScore:
            self._bestSol = parziale[:]
            self._bestScore = self._getScore(parziale)

        for node in nx.neighbors(self._grafo, parziale[-1]):
            if node not in parziale and self._grafo[parziale[-1]][node]["weight"]<self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(node)
                self._ricorsione(parziale)
                parziale.pop()

    def _getScore(self, list):
        sum = 0
        for i in range(len(list)-1):
            sum += self._grafo[list[i]][list[i+1]]["weight"]
        return sum


    def toSoluzione(self, list):
        result = []
        for i in range(len(list)-1):
            result.append((list[i], list[i+1], self._grafo[list[i]][list[i+1]]["weight"]))
        return result