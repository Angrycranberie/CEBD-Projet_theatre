import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from utils import display


# Classe permettant d'afficher la fonction à compléter 6
class AppFctComp6(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_6.ui", self)
        self.data = data
        self.refreshSpecList()
        self.ui.comboBox_fct_comp_6.setCurrentIndex(0)

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_error_fct_comp_6, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT dateRep, case noPlace when null then 0 else count(noPlace) end as nbPlacesReserv "
                "FROM LesRepresentations "
                "NATURAL JOIN LesSpectacles "
                "NATURAL LEFT JOIN LesTickets "
                "WHERE nomSpec = ? "
                "GROUP BY dateRep",
                [self.ui.comboBox_fct_comp_6.currentText()]
            )
        except Exception as e:
            self.ui.table_fct_comp_6.setRowCount(0)
            display.refreshLabel(self.ui.label_error_fct_comp_6, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_comp_6, result)



    # Fonction de récupération des spectacles
    def refreshSpecList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT nomSpec FROM LesSpectacles")
        except Exception as e:
            self.ui.comboBox_fct_comp_6.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_comp_6, result)
