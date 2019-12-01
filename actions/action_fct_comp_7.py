import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from utils.display import refreshGenericCombo


# Classe permettant d'afficher la fonction à compléter 7
class AppFctComp7(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_7.ui", self)
        self.data = data
        self.refreshResult()
        self.refreshSpecList()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_comp_7, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec, dateRep, promoRep, nbPlacesDispoRep FROM LesRepresentations")
        except Exception as e:
            self.ui.table_fct_comp_7.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_comp_7, result)

    @pyqtSlot()
    def refreshSpecList(self):
        print("test")
        try:
            print("try passed")
            cursor = self.data.cursor()
            print("cursor")
            result = cursor.execute("SELECT noSpec FROM LesSpectacles")
            print("result")
        except Exception as e:
            self.ui.comboBox_ajout.clear()
            display.refreshLabel(self.ui.label_fct_comp_7, "Aucune catégorie trouvée")
        else:
            print("excep")
            display.refreshGenericCombo(self.ui.comboBox_ajout, result)



    def ajouter(self):
        display.refreshLabel(self.ui.label_fct_comp_7, "")
        spec = str(self.ui.comboBox_ajout.currentText())
        try:
            # cursor = self.data.cursor()
            # result = cursor.execute("INSERT INTO LesRepresentations (noSpec, dateRep, promoRep)" VALUES ())
            print(spec)
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))