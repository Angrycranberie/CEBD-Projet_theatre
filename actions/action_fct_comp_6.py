import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fonction à compléter 6
class AppFctComp6(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_6.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        # display.refreshLabel(self.ui.label_fct_comp_6, "")
        try:
            pass
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec, dateRep, case noPlace when null then 0 else count(noPlace) end as nbPlacesReserv FROM LesRepresentations NATURAL LEFT JOIN LesTickets GROUP BY noSpec, dateRep")
        except Exception as e:
            self.ui.table_fct_comp_6.setRowCount(0)
            # display.refreshLabel(self.ui.label_fct_comp_6, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_comp_6, result)
