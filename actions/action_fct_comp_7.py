import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import time
from datetime import datetime


# Classe permettant d'afficher la fonction à compléter 7
class AppFctComp7(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_7.ui", self)
        self.formatTable([200, 120, 70, 50])
        self.data = data
        self.refreshResult()
        self.refreshSpecList()
        self.refreshSpec_suppr_List()
        self.refreshRepr_suppr_List()

    # Fonction de mise en forme de la table
    def formatTable(self, columnsize):
        display.setColumnSize(self.ui.table_fct_comp_7, columnsize)
        self.ui.table_fct_comp_7.setMinimumSize(sum(columnsize) + 20, 400)

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_comp_7, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, dateRep, promoRep, nbPlacesDispoRep "
                "FROM LesRepresentations "
                "NATURAL JOIN LesSpectacles"
            )
        except Exception as e:
            self.ui.table_fct_comp_7.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_comp_7, result)

    # mise à jour de la combo box des ajouts
    def refreshSpecList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT nomSpec FROM LesSpectacles")
            # result2 = result
        except Exception as e:
            self.ui.comboBox_ajout_fct_comp_7.clear()
            # self.ui.comboBox_suppr_fct_comp_7.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_ajout_fct_comp_7, result)
            # display.refreshGenericCombo(self.ui.comboBox_suppr_fct_comp_7, result2)

    # mise à jour de la combo box des suppressions pour les noSpec
    def refreshSpec_suppr_List(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT nomSpec FROM LesSpectacles")
        except Exception as e:
            self.ui.comboBox_suppr_fct_comp_7.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_suppr_fct_comp_7, result)

    # mise à jour de la combo box des suppressions pour les dateRep
    def refreshRepr_suppr_List(self):
        try:
            cursor = self.data.cursor()
            # requête avec paramètre '?'
            result = cursor.execute(
                "SELECT dateRep FROM LesRepresentations NATURAL JOIN LesSpectacles WHERE nomSpec = ? ",
                [str(self.ui.comboBox_suppr_fct_comp_7.currentText())])
        except Exception as e:
            self.ui.comboBox_suppr_fct_comp_7_2.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_suppr_fct_comp_7_2, result)

    # ajout d'une représentation dans la table
    def ajouter(self):
        display.refreshLabel(self.ui.label_fct_comp_7, "")
        try:
            cursor = self.data.cursor()
            # conditions pour que l'ajout ce fasse et que on ne peut pas vérifier en SQL
            if self.ui.comboBox_ajout_fct_comp_7.currentText() == "":
                raise Exception("no Spec")
            result = cursor.execute("SELECT dateRep FROM LesRepresentations WHERE dateRep = ?",
                                    [str(self.ui.dateTimeEdit.date())])
            print(list(result))
            if len(result.fetchall()) != 0:
                raise Exception("Representation existante ou salle prise")
            if self.ui.doubleSpinBox.value() > 1 or self.ui.doubleSpinBox.value() <= 0:
                raise Exception("Promo doit être compris entre 0 et 1")

            # récupération du noSpec
            noSpecReq = cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?",
                                       [str(self.ui.comboBox_ajout_fct_comp_7.currentText())])
            noSpecRepr = list(noSpecReq)[0][0]

            # récupération de la dateRep
            dateRepr = self.ui.dateTimeEdit.dateTime().toPyDateTime()
            dateRepr = dateRepr.strftime("%d/%m/%Y %H:%M")

            result = cursor.execute("INSERT INTO LesRepresentations_base (noSpec, dateRep, promoRep) VALUES(?, ?, ?)",
                                    [int(noSpecRepr), dateRepr, self.ui.doubleSpinBox.value()])

            # mise à jour persistante de la base de donnée
            result = cursor.execute("COMMIT")
            self.refreshResult()
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))

    # suppression d'une représentation
    def suppr(self):
        display.refreshLabel(self.ui.label_fct_comp_7, "")
        try:
            cursor = self.data.cursor()
            noSpecReq = cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?",
                                       [str(self.ui.comboBox_ajout_fct_comp_7.currentText())])

            # récupération du noSpec
            noSpec = list(noSpecReq)[0][0]

            # récupérationn de la dateRep
            dateRepr = self.ui.comboBox_suppr_fct_comp_7_2.currentText()

            #suppréssion de la représentation
            result = cursor.execute("DELETE FROM LesRepresentations_base WHERE noSpec = ? AND dateRep = ?",
                                    [noSpec, dateRepr])
            # suppression des tickets de cette représentaions
            result = cursor.execute("DELETE FROM LesTickets WHERE noSpec = ? AND dateRep = ?", [noSpec, dateRepr])

            result = cursor.execute("DELETE FROM LesDossiers_base WHERE noDos not in (SELECT noDos from LesTickets)")

            # mise à jour persistante de la base de donnée
            result = cursor.execute("COMMIT")
            self.refreshResult()
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
