import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.ui.table_fct_comp_4.setColumnWidth(0, 50)
        self.ui.table_fct_comp_4.setColumnWidth(1, 100)
        self.ui.table_fct_comp_4.setColumnWidth(2, 50)
        self.ui.table_fct_comp_4.setColumnWidth(3, 50)
        self.ui.table_fct_comp_4.setColumnWidth(4, 120)
        self.ui.table_fct_comp_4.setColumnWidth(5, 50)
        self.data = data
        self.refreshDosList()
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
