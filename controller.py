from model import DatabaseModel
import time
import requests
from PyQt6.QtGui import QFont, QPixmap

from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import QUrl, QByteArray, pyqtSignal, QObject
from PyQt6.QtCore import Qt




class DataController:
    def __init__(self, ui):
        self.ui = ui  # Référence à l'interface
        self.model = DatabaseModel()  # Initialiser le modèle de base de données


        
        




    def load_initial_options(self):
        """Charge les options initiales pour le premier champ de sélection."""
        accounts_data = self.model.fetch_accounts()



        # Simuler un délai pour le chargement des options initiales
        
        
        for item_id, name, account_logo in accounts_data:
            self.ui.accounts_dropdown.addItem(name, (item_id,account_logo))

        # Masquer l'indicateur de chargement après le chargement des options
        self.ui.hide_loading_indicator()

    def update_projects_options(self):
        """Met à jour le deuxième champ en fonction de la sélection du premier."""
        selected_id, account_logo_url = self.ui.accounts_dropdown.currentData()
        self.ui.projects_dropdown.setEnabled(bool(selected_id))  # Activer/désactiver le deuxième champ


        if selected_id:
            new_options = self.model.fetch_projects(selected_id)

            # Nettoyer et mettre à jour le deuxième menu
            self.ui.projects_dropdown.clear()
            for item_id, name, project_logo_url in new_options:
                self.ui.projects_dropdown.addItem(name, (item_id,project_logo_url))
        else:
            self.ui.projects_dropdown.clear()


        if account_logo_url:
            pixmap = load_image_from_url(account_logo_url)
            if pixmap:
                # Redimensionner l'image
                pixmap = pixmap.scaled(self.ui.account_image.width(), self.ui.account_image.height(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                self.ui.account_image.setPixmap(pixmap)
                self.ui.account_image.setEnabled(True)
                
            else:
                self.ui.account_image.clear()
        else:
            self.ui.account_image.clear()  # Supprime l'image si erreur
        # self.ui.account_image.setPixmap(QPixmap(account_logo_url))
        # self.ui.account_image.setEnabled(bool(account_logo_url))
    
    
    def update_groupcampaigns_options(self):
        """Met à jour le deuxième champ en fonction de la sélection du premier."""
        selected_account_id, account_logo_url = self.ui.accounts_dropdown.currentData()
        selected_project_id, project_logo_url = self.ui.projects_dropdown.currentData()
        # self.ui.groupcampaigns_dropdown.setEnabled(bool(selected_project_id))  # Activer/désactiver le deuxième champ
        print("test1")

        if selected_project_id:
            print("test2")
            new_options = self.model.fetch_groupcampaigns(selected_project_id,selected_account_id)

        #     # Nettoyer et mettre à jour le deuxième menu
        #     self.ui.groupcampaigns_dropdown.clear()
        #     for item_id, name in new_options:
        #         self.ui.groupcampaigns_dropdown.addItem(name, item_id)
        # else:
        #     self.ui.groupcampaigns_dropdown.clear()


        if project_logo_url:
            print("test3")
            pixmap = load_image_from_url(project_logo_url)
            if pixmap:
                # Redimensionner l'image
                pixmap = pixmap.scaled(self.ui.project_image.width(), self.ui.project_image.height(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                self.ui.project_image.setPixmap(pixmap)
                self.ui.project_image.setEnabled(True)
                
            else:
                self.ui.project_image.clear()
        else:
            self.ui.project_image.clear()  # Supprime l'image si erreur
        # self.ui.account_image.setPixmap(QPixmap(account_logo_url))
        # self.ui.account_image.setEnabled(bool(account_logo_url))




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