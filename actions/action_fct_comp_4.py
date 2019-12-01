import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from utils import display


# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.formatTable([50, 100, 50, 50, 120, 50])
        self.data = data
        self.refreshDosList()
        self.ui.listWidget_4_dossier.setCurrentItem(self.ui.listWidget_4_dossier.item(0))
        self.refreshCatList()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT * FROM LesTickets NATURAL JOIN LesPlaces NATURAL JOIN LesZones WHERE noDos = ? AND catZone=?",
                [self.ui.listWidget_4_dossier.currentItem().text(), self.ui.comboBox_4_categorie.currentText()]
            )
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT catZone FROM LesZones NATURAL JOIN LesPlaces NATURAL JOIN LesTickets WHERE noDos = ?",
                [self.ui.listWidget_4_dossier.currentItem().text()]
            )
        except Exception as e:
            self.ui.comboBox_4_categorie.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_4_categorie, result)

    # Fonction de mise à jour des dossiers
    @pyqtSlot()
    def refreshDosList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noDos FROM LesDossiers_base")
        except Exception as e:
            self.ui.listWidget_4_dossier.clear()
        else:
            display.refreshGenericListWidget(self.ui.listWidget_4_dossier, result)

    def formatTable(self, columnsize):
        display.setColumnSize(self.ui.table_fct_comp_4, columnsize)
        self.ui.table_fct_comp_4.setMinimumWidth(sum(columnsize) + 20)