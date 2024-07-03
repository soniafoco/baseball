import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedYear = None


    def handleDDYear(self, e):
        self._view._txtOutSquadre.controls.clear()
        self._selectedYear = self._view._ddAnno.value
        if self._selectedYear is None:
            self._view._txtOutSquadre.controls.append(ft.Text("Selezionare un anno!"))
            self._view.update_page()
            return

        squadre = self._model.getSquadreAnno(self._selectedYear)
        if len(squadre) == 0:
            self._view._txtOutSquadre.controls.append(ft.Text("Non ci sono squadre che hanno partecipato in questo anno"))
            self._view.update_page()
            return

        self._view._txtOutSquadre.controls.append(ft.Text(f"Ci sono {len(squadre)} squadre che hanno partecipato:"))
        for squadra in squadre:
            self._view._txtOutSquadre.controls.append(ft.Text(squadra))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=squadra, text=squadra.__str__(), on_click=self.readDDsquadra))
        self._view.update_page()

    def readDDsquadra(self, e):
        self._selectedSquadra = e.control.data
        print(self._selectedSquadra)

    def fillDDYears(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(int(year)))

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        self._selectedYear = self._view._ddAnno.value
        if self._selectedYear is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare un anno!"))
            self._view.update_page()
            return

        self._model.creaGrafo(self._selectedYear)

        node, edges = self._model.getDettagliGrafo()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato con {node} nodi e {edges} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        if self._selectedSquadra is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare una squadra!"))
            self._view.update_page()
            return

        vicini = self._model.getVicini(self._selectedSquadra)
        if len(vicini) == 0:
            self._view._txt_result.controls.append(ft.Text("Non ci sono nodi adiacenti"))
            return

        self._view._txt_result.controls.append(ft.Text(f"Adiacenti della squadra {self._selectedSquadra}"))
        for node in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{node[0]}     {node[1]}"))
        self._view.update_page()


    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        if self._selectedSquadra is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare una squadra!"))
            self._view.update_page()
            return

        path, score = self._model.getPercorso(self._selectedSquadra)
        self._view._txt_result.controls.append(ft.Text(f"Trovato percorso di peso {score}:"))
        for edge in path:
            self._view._txt_result.controls.append(ft.Text(f"{edge[0]} --> {edge[1]} - peso = {edge[2]}"))
        self._view.update_page()