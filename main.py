
import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

from actions.action_fct_comp_1 import AppFctComp1
from actions.action_fct_comp_2 import AppFctComp2
from actions.action_fct_comp_3 import AppFctComp3
from actions.action_fct_comp_4 import AppFctComp4
from actions.action_fct_comp_5 import AppFctComp5
from actions.action_fct_comp_6 import AppFctComp6
from actions.action_fct_comp_7 import AppFctComp7
from actions.action_fct_comp_8 import AppFctComp8
from actions.action_fct_fournie_1 import AppFctFournie1
from actions.action_fct_fournie_2 import AppFctFournie2
from actions.action_tablesData import AppTablesData
from utils import db
from utils import display


# Classe utilisée pour lancer la fenêtre principale de l'application et définir ses actions
class AppWindow(QMainWindow):

    # Création d'un signal destiné à être émis lorsque la table est modifiée
    changedValue = pyqtSignal()

    # On prévoit des variables pour accueillir les fenêtres supplémentaires
    tablesDataDialog = None
    fct_fournie_1_dialog = None
    fct_fournie_2_dialog = None
    fct_comp_1_dialog = None
    fct_comp_2_dialog = None
    fct_comp_3_dialog = None
    fct_comp_4_dialog = None
    fct_comp_5_dialog = None
    fct_comp_6_dialog = None
    fct_comp_7_dialog = None
    fct_comp_8_dialog = None

    # Constructeur
    def __init__(self):

        # On appelle le constructeur de la classe dont on hérite
        super(AppWindow, self).__init__()

        # On charge le gui de la fenêtre
        self.ui = uic.loadUi("gui/mainWindow.ui", self)

        # On se connecte à la base de données
        self.data = sqlite3.connect("data/theatre.db")

    ####################################################################################################################
    # Définition des actions
    ####################################################################################################################

    # Action en cas de clic sur le bouton de création de base de données
    def createDB(self):

        try:
            # On exécute les requêtes du fichier de création
            db.updateDBfile(self.data, "data/createDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_2, "L'erreur suivante s'est produite pendant lors de la création de la base : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_2, "La base de données a été créée avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton d'insertion de données
    def insertDB(self):

        try:
            # On exécute les requêtes du fichier d'insertion
            db.updateDBfile(self.data, "data/insertDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_2, "L'erreur suivante s'est produite lors de l'insertion des données : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_2, "Un jeu de test a été inséré dans la base avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton de suppression de la base
    def deleteDB(self):

        try:
            # On exécute les requêtes du fichier de suppression
            db.updateDBfile(self.data, "data/deleteDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_2, "Erreur lors de la suppression de la base de données : " + repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès (le commit est automatique pour un DROP TABLE)
            display.refreshLabel(self.ui.label_2, "La base de données a été supprimée avec succès.")
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    ####################################################################################################################
    # Ouverture des autres fenêtres de l'application
    ####################################################################################################################

    # En cas de clic sur le bouton de visualisation des données
    def openData(self):
        if self.tablesDataDialog is not None:
            self.tablesDataDialog.close()
        self.tablesDataDialog = AppTablesData(self.data)
        self.tablesDataDialog.show()
        self.changedValue.connect(self.tablesDataDialog.refreshAllTables)

    # En cas de clic sur la fonction fournie 1
    def open_fct_fournie_1(self):
        if self.fct_fournie_1_dialog is not None:
            self.fct_fournie_1_dialog.close()
        self.fct_fournie_1_dialog = AppFctFournie1(self.data)
        self.fct_fournie_1_dialog.show()
        self.changedValue.connect(self.fct_fournie_1_dialog.refreshResult)

    # En cas de clic sur la fonction fournie 2
    def open_fct_fournie_2(self):
        if self.fct_fournie_2_dialog is not None:
            self.fct_fournie_2_dialog.close()
        self.fct_fournie_2_dialog = AppFctFournie2(self.data)
        self.fct_fournie_2_dialog.show()

    # En cas de clic sur la fonction à compléter 1
    def open_fct_comp_1(self):
        if self.fct_comp_1_dialog is not None:
            self.fct_comp_1_dialog.close()
        self.fct_comp_1_dialog = AppFctComp1(self.data)
        self.fct_comp_1_dialog.show()
        self.changedValue.connect(self.fct_comp_1_dialog.refreshResult)

    # En cas de clic sur la fonction à compléter 2
    def open_fct_comp_2(self):
        if self.fct_comp_2_dialog is not None:
            self.fct_comp_2_dialog.close()
        self.fct_comp_2_dialog = AppFctComp2(self.data)
        self.fct_comp_2_dialog.show()

    # En cas de clic sur la fonction à compléter 3
    def open_fct_comp_3(self):
        if self.fct_comp_3_dialog is not None:
            self.fct_comp_3_dialog.close()
        self.fct_comp_3_dialog = AppFctComp3(self.data)
        self.fct_comp_3_dialog.show()

    # En cas de clic sur la fonction à compléter 4
    def open_fct_comp_4(self):
        if self.fct_comp_4_dialog is not None:
            self.fct_comp_4_dialog.close()
        self.fct_comp_4_dialog = AppFctComp4(self.data)
        self.fct_comp_4_dialog.show()
        self.changedValue.connect(self.fct_comp_4_dialog.refreshCatList)

    # En cas de clic sur la fonction à compléter 5
    def open_fct_comp_5(self):
        if self.fct_comp_5_dialog is not None:
            self.fct_comp_5_dialog.close()
        self.fct_comp_5_dialog = AppFctComp5(self.data)
        self.fct_comp_5_dialog.show()

    def open_fct_comp_6(self):
        if self.fct_comp_6_dialog is not None:
            self.fct_comp_6_dialog.close()
        self.fct_comp_6_dialog = AppFctComp6(self.data)
        self.fct_comp_6_dialog.show()

    def open_fct_comp_7(self):
        if self.fct_comp_7_dialog is not None:
            self.fct_comp_7_dialog.close()
        self.fct_comp_7_dialog = AppFctComp7(self.data)
        self.fct_comp_7_dialog.show()

    def open_fct_comp_8(self):
        if self.fct_comp_8_dialog is not None:
            self.fct_comp_8_dialog.close()
        self.fct_comp_8_dialog = AppFctComp8(self.data)
        self.fct_comp_8_dialog.show()


    ####################################################################################################################
    # Fonctions liées aux évènements (signal/slot/event)
    ####################################################################################################################
    # TODO 3 : penser à fermer comme il faut les fenêtres de la partie 3

    # On intercepte l'évènement de cloture de la fenêtre principale pour intercaler quelques actions avant sa fermeture
    def closeEvent(self, event):

        # On ferme les éventuelles fenêtres encore ouvertes
        if self.tablesDataDialog is not None:
            self.tablesDataDialog.close()
        if self.fct_fournie_1_dialog is not None:
            self.fct_fournie_1_dialog.close()
        if self.fct_fournie_2_dialog is not None:
            self.fct_fournie_2_dialog.close()
        if self.fct_comp_1_dialog is not None:
            self.fct_comp_1_dialog.close()
        if self.fct_comp_2_dialog is not None:
            self.fct_comp_2_dialog.close()
        if self.fct_comp_3_dialog is not None:
            self.fct_comp_3_dialog.close()
        if self.fct_comp_4_dialog is not None:
            self.fct_comp_4_dialog.close()
        if self.fct_comp_5_dialog is not None:
            self.fct_comp_5_dialog.close()
        if self.fct_comp_6_dialog is not None:
            self.fct_comp_6_dialog.close()
        if self.fct_comp_7_dialog is not None:
            self.fct_comp_7_dialog.close()
        if self.fct_comp_8_dialog is not None:
            self.fct_comp_8_dialog.close()

        # On ferme proprement la base de données
        self.data.close()

        # On laisse l'évènement de clôture se terminer normalement
        event.accept()

# Lancement de la fenêtre principale
app = QApplication(sys.argv)
MainWindow = AppWindow()
MainWindow.show()
sys.exit(app.exec_())