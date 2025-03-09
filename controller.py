from model import DatabaseModel
import time
import requests
from PyQt6.QtGui import QFont, QPixmap

from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import QUrl, QByteArray, pyqtSignal, QObject
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem

import re




class DataController:
    def __init__(self, ui):
        self.ui = ui  # Référence à l'interface
        self.model = DatabaseModel()  # Initialiser le modèle de base de données


        
        




    def load_initial_options(self):
        """Charge les options initiales pour le premier champ de sélection."""
        accounts_data = self.model.fetch_accounts()



        # Simuler un délai pour le chargement des options initiales
        
        
        for item_id, name, account_logo in accounts_data:
            self.ui.account_widget.accounts_dropdown.addItem(name, (item_id,account_logo))

        self.ui.account_id_selected = self.ui.account_widget.accounts_dropdown.currentIndex()
        self.ui.account_name_selected = self.ui.account_widget.accounts_dropdown.currentText()

        # Masquer l'indicateur de chargement après le chargement des options
        self.ui.hide_loading_indicator()

    def update_projects_options(self):
        """Met à jour le deuxième champ en fonction de la sélection du premier."""
        selected_id, account_logo_url = self.ui.account_widget.accounts_dropdown.currentData()
        self.ui.group_campaign_table.model.removeRows(0, self.ui.group_campaign_table.model.rowCount())

        #sauvergarde des data selectionnées
        self.ui.account_id_selected = selected_id
        self.ui.account_name_selected = self.ui.account_widget.accounts_dropdown.currentText()
        

        self.ui.project_widget.projects_dropdown.blockSignals(True)
        if selected_id:
            new_options = self.model.fetch_projects(selected_id)

            # Nettoyer et mettre à jour le deuxième menu
            self.ui.project_widget.projects_dropdown.clear()
            self.ui.project_widget.project_image.clear()
            self.ui.project_widget.project_image.setEnabled(False)
            
            self.ui.project_widget.projects_dropdown.addItem("Selectionnez le projet..", (-1,""))
            for item_id, name, project_logo_url in new_options:
                self.ui.project_widget.projects_dropdown.addItem(name, (item_id,project_logo_url))
        else:
            
            self.ui.project_widget.projects_dropdown.clear()
            self.ui.project_widget.project_image.clear()
            self.ui.project_widget.project_image.setEnabled(False)
            
        self.ui.project_widget.projects_dropdown.blockSignals(False)
        self.ui.project_widget.projects_dropdown.setEnabled(bool(selected_id))
        self.ui.project_widget.add_project_button.setEnabled(bool(selected_id))  # Activer/désactiver le deuxième champ


        if account_logo_url:
            pixmap = load_image_from_url(account_logo_url)
            if pixmap:
                # Redimensionner l'image
                pixmap = pixmap.scaled(self.ui.account_widget.account_image.width(), self.ui.account_widget.account_image.height(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                self.ui.account_widget.account_image.setPixmap(pixmap)
                self.ui.account_widget.account_image.setEnabled(True)
                
            else:
                self.ui.account_widget.account_image.clear()
        else:
            self.ui.account_widget.account_image.clear()  # Supprime l'image si erreur
        # self.ui.account_image.setPixmap(QPixmap(account_logo_url))
        # self.ui.account_image.setEnabled(bool(account_logo_url))
    
    
    def update_groupcampaigns_options(self):
        """Met à jour le deuxième champ en fonction de la sélection du premier."""
        selected_account_id, account_logo_url = self.ui.account_widget.accounts_dropdown.currentData()
        print("lancement de l'update des groupcampaigns")
        self.ui.group_campaign_table.model.removeRows(0, self.ui.group_campaign_table.model.rowCount())

        if not self.ui.project_widget.projects_dropdown.currentData() :
            return
        selected_project_id, project_logo_url = self.ui.project_widget.projects_dropdown.currentData()
        if selected_project_id == -1:
            return
        
        #Enlever le texte par défaut
        
        index = self.ui.project_widget.projects_dropdown.findText("Selectionnez le projet..")
        if index != -1:  # Vérifie que l'élément existe avant de le supprimer
            self.ui.project_widget.projects_dropdown.blockSignals(True)
            self.ui.project_widget.projects_dropdown.removeItem(index)
            self.ui.project_widget.projects_dropdown.blockSignals(False)

        
        # self.ui.groupcampaigns_dropdown.setEnabled(bool(selected_project_id))  # Activer/désactiver le deuxième champ
        if project_logo_url:
            pixmap = load_image_from_url(project_logo_url)
            if pixmap:
                # Redimensionner l'image
                pixmap = pixmap.scaled(self.ui.project_widget.project_image.width(), self.ui.project_widget.project_image.height(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                self.ui.project_widget.project_image.setPixmap(pixmap)
                self.ui.project_widget.project_image.setEnabled(True)
                
            else:
                self.ui.project_widget.project_image.clear()
        else:
            self.ui.project_widget.project_image.clear()  # Supprime l'image si erreur

        if selected_project_id:
            groupscampaingsdata = self.model.fetch_groupcampaigns(selected_project_id,selected_account_id)
            print(groupscampaingsdata)

        for row, values in enumerate(groupscampaingsdata):
            print("les values : ",values)
            print("les row : ",row)
            for col, value in enumerate(values):
                item = QStandardItem(str(value))
                # self.ui.model.setItem(row, col, item))
                if col in self.ui.group_campaign_table.locked_columns:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.ui.group_campaign_table.model.setItem(row, col, item)

        #     # Nettoyer et mettre à jour le deuxième menu
        #     self.ui.groupcampaigns_dropdown.clear()
        #     for item_id, name in new_options:
        #         self.ui.groupcampaigns_dropdown.addItem(name, item_id)
        # else:
        #     self.ui.groupcampaigns_dropdown.clear()



        # self.ui.account_image.setPixmap(QPixmap(account_logo_url))
        # self.ui.account_image.setEnabled(bool(account_logo_url))


    def validate_project_name(self, project_name):
        """Vérifie si le nom du projet est valide."""
        if not project_name.strip():
            return False, "Le champ ne peut pas être vide."

        if len(project_name) > 32:
            return False, "Nom trop long, maximum 32 caractères."

        if not re.match(r'^[a-zA-Z0-9 ]+$', project_name):
            return False, "Caractères spéciaux non autorisés."

        return True, None  
    
    def send_project_to_xano(self,account_id, project_name, logo_path):

        return self.model.post_project(account_id, project_name, logo_path)



    def send_form_data_to_db(self, client, option):
        """Envoie les données du formulaire à la base de données."""
        success = self.model.send_form_data(client, option)
        if success:
            self.ui.show_message("Succès", "Les données ont été envoyées avec succès.")
        else:
            self.ui.show_message("Erreur", "Échec de l'envoi des données.")


    


def load_image_from_url(url):
    """Télécharge une image depuis une URL et retourne un QPixmap."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})  # ✅ Ajoute un User-Agent pour éviter le blocage
        response.raise_for_status()  # ✅ Vérifie si la requête est OK (évite les erreurs 403/404)

        image_data = QByteArray(response.content)  # ✅ Convertir les données en binaire
        pixmap = QPixmap()
        if not pixmap.loadFromData(image_data):  # ✅ Vérifier si PyQt arrive à charger l'image
            print("❌ Erreur : Impossible de charger l’image avec QPixmap")
            return None

        return pixmap

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du téléchargement de l'image : {e}")
        return None