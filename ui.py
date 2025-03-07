from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QProgressBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from controller import DataController

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = DataController(self)  # Contrôleur pour gérer les requêtes
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Application dynamique")
        self.setGeometry(100, 100, 500, 250)

        layout = QVBoxLayout()

        self.add_title(layout)
        self.add_loading_indicator(layout)
        self.add_primary_dropdown(layout)
        self.add_secondary_dropdown(layout)
        self.add_submit_button(layout)

        self.setLayout(layout)

        # Charger les premiers choix
        self.controller.load_initial_options()

        # Connecter le premier dropdown au changement
        self.dropdown1.currentIndexChanged.connect(self.controller.update_secondary_options)

    def add_title(self, layout):
        """Ajoute le titre à la mise en page."""
        title = QLabel("Sélection dynamique")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

    def add_primary_dropdown(self, layout):
        """Ajoute le premier champ de sélection à la mise en page."""
        self.label1 = QLabel("Choisissez un client :")
        self.label1.setFont(QFont("Arial", 12))
        layout.addWidget(self.label1)

        self.dropdown1 = QComboBox()
        layout.addWidget(self.dropdown1)

    def add_secondary_dropdown(self, layout):
        """Ajoute le deuxième champ de sélection à la mise en page."""
        self.label2 = QLabel("Options disponibles :")
        self.label2.setFont(QFont("Arial", 12))
        layout.addWidget(self.label2)

        self.dropdown2 = QComboBox()
        self.dropdown2.setEnabled(False)  # Désactiver initialement
        layout.addWidget(self.dropdown2)

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
