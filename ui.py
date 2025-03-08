from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QProgressBar
from PyQt6.QtGui import QFont, QPixmap, QFontDatabase
from PyQt6.QtCore import Qt
from controller import DataController
import os
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = DataController(self)  # Contrôleur pour gérer les requêtes
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SA Corp - Saas Backoffice")
        self.setGeometry(100, 100, 1500, 700)

        font_files = [
            "Gilroy-Regular.ttf",
            "Gilroy-Bold.ttf",
            "Gilroy-Light.ttf",
            "Gilroy-Thin.ttf"
        ]


        # Détecter si l'application est compilée
        if getattr(sys, 'frozen', False):
            print("yes")
            assets_path = os.path.join(os.path.dirname(sys.executable), "..", "Resources", "assets","font")
            font_path = assets_path #os.path.join(assets_path, "font/Gilroy-Regular.ttf")
            print(font_path)
        else:
            print("no")
            font_path = os.path.abspath("assets/font/")
        


        font_families = set()
        for font_file in font_files:
            font_path_temp = os.path.join(font_path, font_file)  # 🔹 Mets le bon chemin
            print(font_path)
            font_id = QFontDatabase.addApplicationFont(font_path_temp)

            if font_id == -1:
                print(f"❌ Erreur : Impossible de charger {font_file}")
            else:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                font_families.add(family)
                print(f"✅ Police chargée : {family}")

        # ✅ Vérifier la famille de police trouvée
        if font_families:
            self.main_font_family = list(font_families)[0]  # 🔹 On prend la première famille
            print(f"✅ Utilisation de la famille : {self.main_font_family}")
        

        self.font_regular = QFont(self.main_font_family, 12)
        self.font_bold = QFont(self.main_font_family, 12, QFont.Weight.Bold)
        self.font_light = QFont(self.main_font_family, 12, QFont.Weight.Light)
        self.font_thin = QFont(self.main_font_family, 12, QFont.Weight.Thin)


        self.setFont(self.font_thin)


        
        # font_id = QFontDatabase.addApplicationFont(font_path)
        # if font_id == -1:
        #     print("❌ Erreur : Impossible de charger la police")
        # else:
        #     font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        #     print(f"✅ Police chargée : {font_family}")
        #     self.setFont(QFont(font_family, 12))  # Taille 12 par défaut pour toute l'application

        

        # Création d'un QLabel pour l'image
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("image.png"))  # Remplacez par le chemin de votre image
        self.label.setScaledContents(True)  # Ajuste l'image à la taille du QLabel

        layout = QVBoxLayout()

        self.add_title(layout)
        self.add_loading_indicator(layout)
        self.add_accounts_dropdown(layout)
        self.add_accounts_info(layout)
        self.add_secondary_dropdown(layout)
        self.add_submit_button(layout)

        self.setLayout(layout)

        # Charger les premiers choix
        self.controller.load_initial_options()

        # Connecter le premier dropdown au changement
        self.accounts_dropdown.currentIndexChanged.connect(self.controller.update_projects_options)

    def add_title(self, layout):
        """Ajoute le titre à la mise en page."""
        title = QLabel("Selection de données du SAAS Xano")
        title.setFont(QFont(self.main_font_family, 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

    def add_accounts_dropdown(self, layout):
        """Ajoute le premier champ de sélection à la mise en page."""
        self.label1 = QLabel("Choisissez un client :")
        self.label1.setFont(self.font_bold)
        layout.addWidget(self.label1)

        self.accounts_dropdown = QComboBox()
        layout.addWidget(self.accounts_dropdown)

    def add_accounts_info(self, layout):
            self.account_image = QLabel(self)
            self.account_image.setScaledContents(False)   # Ajuste l'image à la taille du QLabel

            self.account_image.setGeometry(50, 50, 50, 50)
            self.account_image.setFixedSize(50, 50)
            self.account_image.setStyleSheet("""
                
            """)
            self.account_image.setScaledContents(True)
            
            self.account_image.setEnabled(False)
            layout.addWidget(self.account_image)



    def add_secondary_dropdown(self, layout):
        """Ajoute le deuxième champ de sélection à la mise en page."""
        self.label2 = QLabel("Options disponibles :")
        self.label2.setFont(QFont("Arial", 12))
        layout.addWidget(self.label2)

        self.projects_dropdown = QComboBox()
        self.projects_dropdown.setEnabled(False)  # Désactiver initialement
        layout.addWidget(self.projects_dropdown)

    def add_submit_button(self, layout):
        """Ajoute le bouton de soumission à la mise en page."""
        submit_button = QPushButton("Soumettre")
        submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(submit_button)

    def add_loading_indicator(self, layout):
        """Ajoute un indicateur de chargement à la mise en page."""
        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)  # Indicateur de chargement infini
        layout.addWidget(self.loading_bar)

    def hide_loading_indicator(self):
        """Masque l'indicateur de chargement."""
        self.loading_bar.hide()

    def handle_submit(self):
        """Vérifie les données sélectionnées et affiche un message."""
        client = self.dropdown1.currentText()
        option = self.dropdown2.currentText()

        if not client or not option:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client et une option.")
        else:
            self.controller.send_form_data_to_db(client, option)

    def show_message(self, title, message):
        """Affiche un message à l'utilisateur."""
        QMessageBox.information(self, title, message)
