import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from utils import display


# Classe permettant d'afficher la fonction à compléter 8
class AppFctComp8(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_8.ui", self)
        self.formatTable([50, 250, 100, 50, 50, 100, 120, 60])
        self.ui.groupBox_delete_fct_comp_8.setHidden(True)
        self.data = data
        # Tableau des éléments pour l'ajout
        self.addelements = [
            self.ui.comboBox_spec_fct_comp_8,
            self.ui.comboBox_date_fct_comp_8,
            self.ui.comboBox_rang_fct_comp_8,
            self.ui.comboBox_plac_fct_comp_8,
            self.ui.comboBox_redu_fct_comp_8,
            self.ui.pushButton_ajout_fct_comp_8
        ]
        for a in self.addelements:
            a.setEnabled(True)
        self.refreshResult()
        self.refreshSpecList()
        self.refreshReducList()
        self.refreshCurrentFolder()

    # Fonction de mise à jour des résultats
    def refreshResult(self):
        sort = ["nomSpec, dateRep", "noDos"]
        display.refreshLabel(self.ui.label_error_fct_comp_8, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT noDos, nomSpec, dateRep, noPlace, noRang, libelleCat, dateEmTick, prixTicket "
                "FROM LesTickets_extension "
                "NATURAL JOIN LesSpectacles "
                "ORDER BY " + sort[1 if self.ui.radioButton_tri_dos_fct_comp_8.isChecked() else 0]
            )
        except Exception as e:
            self.ui.table_fct_comp_8.setRowCount(0)
            display.refreshLabel(self.ui.label_error_fct_comp_8, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_comp_8, result)

    # Fonction de mise en forme de la table
    def formatTable(self, columnsize):
        display.setColumnSize(self.ui.table_fct_comp_8, columnsize)
        self.ui.table_fct_comp_8.setMinimumSize(sum(columnsize) + 20, 400)

    # Fonction de mise à jour du dossier courant
    def refreshCurrentFolder(self):
        try:
            cursor = self.data.cursor()
            dosMax = list(cursor.execute("SELECT max(noDos) FROM LesDossiers_base"))[0][0]
            dosMaxCount = list(cursor.execute("SELECT count(noDos) FROM LesTickets WHERE noDos = ?", [dosMax]))[0][0]
        except Exception as e:
            display.refreshLabel(self.ui.label_dos_fct_comp_8, "Dossier courant erroné.")
            self.ui.pushButton_newdos_fct_comp_8.setEnabled(False)
        else:
            display.refreshLabel(self.ui.label_dos_fct_comp_8, "Dossier courant : n°" + str(dosMax))
            if dosMaxCount == 0:
                self.ui.pushButton_newdos_fct_comp_8.setEnabled(False)
            else:
                self.ui.pushButton_newdos_fct_comp_8.setEnabled(True)

    # Fonction permettant l'ajout d'un nouveau dossier
    def addFolder(self):
        try:
            cursor = self.data.cursor()
            cursor.execute(
                "INSERT INTO LesDossiers_base(noDos) "
                "VALUES ((SELECT max(noDos)+1 FROM LesDossiers_base))"
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_error_fct_comp_8, "Erreur lors de la création du dossier : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_error_fct_comp_8, "Nouveau dossier créé avec succès.")
            self.refreshCurrentFolder()

    # Fonction de mise à jour de la liste des spectacles
    def refreshSpecList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT nomSpec FROM LesSpectacles "
                "NATURAL JOIN LesRepresentations "
                "WHERE nbPlacesDispoRep > 0"
            )
        except Exception as e:
            self.ui.comboBox_spec_fct_comp_8.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_spec_fct_comp_8, result)
            if self.ui.comboBox_spec_fct_comp_8.currentText() == '':
                display.refreshLabel(self.ui.label_error_fct_comp_8, "Il n'y a plus de places disponibles.")
                for a in self.addelements:
                    a.setEnabled(False)
                    if a != self.ui.pushButton_ajout_fct_comp_8:
                        a.clear()

    # Fonction de mise à jour de la liste des dates de représentations
    def refreshDateList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT dateRep FROM LesRepresentations "
                "NATURAL JOIN LesSpectacles "
                "WHERE nomSpec = ? "
                "AND nbPlacesDispoRep > 0",
                [self.ui.comboBox_spec_fct_comp_8.currentText()]
            )
        except Exception as e:
            self.ui.comboBox_date_fct_comp_8.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_date_fct_comp_8, result)

    # Fonction de mise à jour de la liste des rangs
    def refreshRowList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT noRang "
                "FROM LesPlaces "
                "WHERE noPlace || '_' || noRang "
                "NOT IN ( "
                "SELECT noPlace || '_' || noRang "
                "FROM LesTickets "
                "NATURAL JOIN LesSpectacles "
                "WHERE nomSpec = ? AND dateRep = ? "
                ") "
                "ORDER BY noRang",
                [self.ui.comboBox_spec_fct_comp_8.currentText(), self.ui.comboBox_date_fct_comp_8.currentText()]
            )
        except Exception as e:
            self.ui.comboBox_rang_fct_comp_8.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_rang_fct_comp_8, result)

    # Fonction de mise à jour de la liste des rangs
    def refreshPlacList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT noPlace "
                "FROM LesPlaces "
                "WHERE noPlace || '_' || noRang "
                "NOT IN ( "
                "SELECT noPlace || '_' || noRang "
                "FROM LesTickets "
                "NATURAL JOIN LesSpectacles "
                "WHERE nomSpec = ? AND dateRep = ? "
                ") AND noRang = ?"
                "ORDER BY noPlace",
                [
                    self.ui.comboBox_spec_fct_comp_8.currentText(),
                    self.ui.comboBox_date_fct_comp_8.currentText(),
                    self.ui.comboBox_rang_fct_comp_8.currentText()
                ]
            )
        except Exception as e:
            self.ui.comboBox_plac_fct_comp_8.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_plac_fct_comp_8, result)

    # Fonction de mise à jour de la liste des réductions
    def refreshReducList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT libelleCat FROM LesCategoriesTickets")
        except Exception as e:
            self.ui.comboBox_redu_fct_comp_8.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_redu_fct_comp_8, result)

    # Fonction d'ajout d'une réservation dans la BDD
    def addReservation(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "INSERT INTO LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos, libelleCat) "
                "VALUES ((SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?), "
                "?, ?, ?, strftime('%d/%m/%Y %H:%M:%S','now'), (SELECT max(noDos) FROM LesDossiers_base), ?)",
                [
                    self.ui.comboBox_spec_fct_comp_8.currentText(),
                    self.ui.comboBox_date_fct_comp_8.currentText(),
                    self.ui.comboBox_plac_fct_comp_8.currentText(),
                    self.ui.comboBox_rang_fct_comp_8.currentText(),
                    self.ui.comboBox_redu_fct_comp_8.currentText()
                ]
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_error_fct_comp_8, "Impossible d'insérer la réservation : " + repr(e))
        else:
            self.refreshResult()
            display.refreshLabel(self.ui.label_error_fct_comp_8, "Réservation insérée avec succès.")
            self.refreshSpecList()
            self.refreshCurrentFolder()

    # Fonction démarrant la suppression d'un réservation
    def deleteReservation(self):
        display.refreshLabel(self.ui.label_error_fct_comp_8, "")
        cr = self.ui.table_fct_comp_8.currentRow()
        if cr != -1:
            self.ui.groupBox_delete_fct_comp_8.setHidden(False)
            self.ui.pushButton_delete_fct_comp_8.setEnabled(False)
            self.ui.table_fct_comp_8.selectRow(cr)
            nodos = self.ui.table_fct_comp_8.item(cr, 0).text()
            ticketid = [self.ui.table_fct_comp_8.item(cr, i).text() for i in range(1, 5)]
            libcat = self.ui.table_fct_comp_8.item(cr, 5).text()
            display.refreshLabel(
                self.ui.label_delrow_fct_comp_8,
                "[Dossier n°" + nodos + "] Ticket " + libcat + " pour " + ticketid[0] + " le "
                + ticketid[1] + " (rang " + ticketid[3] + ", place " + ticketid[2] + ") "
            )
        else:
            display.refreshLabel(self.ui.label_error_fct_comp_8,
                                 "Sélectionnez une réservation dans le tableau pour la supprimer.")

    # Confirmation de la suppression d'une réservation
    def deleteYes(self):
        self.ui.groupBox_delete_fct_comp_8.setHidden(True)
        display.refreshLabel(self.ui.label_delrow_fct_comp_8, "")
        cr = self.ui.table_fct_comp_8.currentRow()
        nodos = self.ui.table_fct_comp_8.item(cr, 0).text()
        ticketid = [self.ui.table_fct_comp_8.item(cr, i).text() for i in range(1, 5)]
        cursor = self.data.cursor()
        try:
            cursor.execute(
                "DELETE FROM LesTickets "
                "WHERE noSpec = (SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?) "
                "AND dateRep = ? AND noPlace = ? AND noRang = ?",
                ticketid
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_error_fct_comp_8, "Impossible de supprimer la réservation : " + repr(e))
        else:
            try:
                ctfolder = cursor.execute("SELECT count(noDos) FROM LesTickets WHERE noDos = ?", [nodos])
            except Exception as e:
                display.refreshLabel(self.ui.label_error_fct_comp_8, "Parcours des dossiers erroné : " + repr(e))
            else:
                if list(ctfolder)[0][0] == 0:
                    try:
                        cursor.execute("DELETE FROM LesDossiers_base WHERE noDos = ?", [nodos])
                    except Exception as e:
                        display.refreshLabel(self.ui.label_error_fct_comp_8,
                                             "Impossible de supprimer le dossier : " + repr(e))
                    self.refreshCurrentFolder()
                self.refreshSpecList()
                self.refreshResult()
                display.refreshLabel(self.ui.label_error_fct_comp_8, "Suppression effectuée avec succès.")

        self.ui.table_fct_comp_8.selectRow(-1)
        self.ui.pushButton_delete_fct_comp_8.setEnabled(True)

    # Annulation de la suppression d'une réservation
    def deleteNo(self):
        self.ui.table_fct_comp_8.selectRow(-1)
        self.ui.groupBox_delete_fct_comp_8.setHidden(True)
        self.ui.pushButton_delete_fct_comp_8.setEnabled(True)
