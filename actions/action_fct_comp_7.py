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
        self.refreshSpec_suppr_List()
        self.refreshRepr_suppr_List()

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

    def refreshSpec_suppr_List(self):
            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT nomSpec FROM LesSpectacles")
            except Exception as e:
                self.ui.comboBox_suppr_fct_comp_7.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_suppr_fct_comp_7, result)

    def refreshRepr_suppr_List(self):
            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT dateRep FROM LesRepresentations NATURAL JOIN LesSpectacles WHERE nomSpec = ? ",
                                        [str(self.ui.comboBox_suppr_fct_comp_7.currentText())])
            except Exception as e:
                self.ui.comboBox_suppr_fct_comp_7_2.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_suppr_fct_comp_7_2, result)


    def ajouter(self):
        display.refreshLabel(self.ui.label_fct_comp_7, "")
        spec = str(self.ui.comboBox_ajout_fct_comp_7.currentText())
        try:
            cursor = self.data.cursor()
            print(spec)
            if self.ui.comboBox_ajout_fct_comp_7.currentText() == "":
                raise Exception("no Spec")
            result = cursor.execute("SELECT dateRep FROM LesRepresentations WHERE dateRep = ?", [str(self.ui.dateTimeEdit.date())])
            print(list(result))
            if len(result.fetchall()) != 0:
                raise Exception("Representation existante ou salle prise")
            if self.ui.doubleSpinBox.value() > 1 or self.ui.doubleSpinBox.value() <= 0:
                raise Exception("Promo doit être compris entre 0 et 1")

            noSpecReq = cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", [str(self.ui.comboBox_ajout_fct_comp_7.currentText())])
            noSpecRepr = list(noSpecReq)[0][0]
            dateRepr = self.ui.dateTimeEdit.date()
            result = cursor.execute("INSERT INTO LesRepresentations_base (noSpec, dateRep, promoRep) VALUES(?, ?, ?)", [noSpecRepr, self.ui.dateTimeEdit.date(), self.ui.doubleSpinBox.value()])

        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
