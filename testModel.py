from model.model import Model

m = Model()
m.getSquadreAnno(2015)
m.creaGrafo(2015)
path, score = m.getPercorso(list(m._grafo.nodes)[0])

for p in path:
    print(p)