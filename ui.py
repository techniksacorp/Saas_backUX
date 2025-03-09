from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QProgressBar,  QTableView,QDialog, QHBoxLayout, QSizePolicy, QFrame,QLineEdit, QFileDialog,QMenuBar,QMenu
from PyQt6.QtGui import QFont, QPixmap, QFontDatabase

from PyQt6.QtGui import QPainter, QBrush, QRegion,QAction
from PyQt6.QtCore import QRect, QSize

from PyQt6.QtGui import QStandardItemModel, QStandardItem

from PyQt6.QtCore import Qt
from controller import DataController
import os
import sys
import re #carractere authorisé

from tools.font_manager import FontManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = DataController(self)  # Contrôleur pour gérer les requêtes
        self.font_manager = FontManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SA Corp - Saas Backoffice")
        self.setGeometry(100, 100, 1500, 700)
        self.setFont(self.font_manager.get_font("regular", 12)) 



       

        layout = QVBoxLayout()
        
        # Ajouter une barre de menu
        self.menu_bar = QMenuBar(self)

        # Créer un menu "Fichier"
        file_menu = self.menu_bar.addMenu("Fichier")
        open_action = QAction("Ouvrir", self)
        save_action = QAction("Sauvegarder", self)
        exit_action = QAction("Fermer l'application", self)
        # Ajouter des actions
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Ligne de séparation
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        # Créer un menu "Aide"
        help_menu = self.menu_bar.addMenu("Aide")
        about_action = QAction("À propos", self)
        help_menu.addAction(about_action)
        #Ajouter la barre de menu au layout principal
        layout.setMenuBar(self.menu_bar)




        self.add_title(layout)
        self.add_loading_indicator(layout)


        topnav_layout = QHBoxLayout()
        topnav_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.account_widget = AccountWidget(self.font_manager)
        topnav_layout.addWidget(self.account_widget.get_layout())
        self.project_widget = ProjectWidget(self.font_manager)
        topnav_layout.addWidget(self.project_widget.get_layout())
        topnav_layout.addSpacing(40)

        self.group_campaign_table = GroupCampaignTableWidget()
        topnav_layout.addWidget(self.group_campaign_table.get_layout())



        layout.addLayout(topnav_layout)


        # self.add_accounts_dropdown(layout)
        # self.add_account_info(layout)
        # self.add_project_dropdown(layout)
        # self.add_project_info(layout)
        # layout.addWidget(self.table)
        self.add_submit_button(layout)

        self.setLayout(layout)

        # Charger les premiers choix
        self.controller.load_initial_options()

        # Connecter le premier dropdown au changement
        self.account_widget.accounts_dropdown.currentIndexChanged.connect(self.controller.update_projects_options)
        
        self.project_widget.projects_dropdown.currentIndexChanged.connect(self.controller.update_groupcampaigns_options)

        self.project_widget.add_project_button.clicked.connect(
            lambda: self.project_widget.open_add_project_window(self.account_id_selected, self.account_name_selected,self.controller)
        )

    def add_title(self, layout):
        """Ajoute le titre à la mise en page."""
        title = QLabel("Selection de données du SAAS Xano")
        title.setFont(self.font_manager.get_font("bold", 16))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

    # def add_accounts_dropdown(self, layout):
    #     """Ajoute le premier champ de sélection à la mise en page."""

    #     account_main_layout = QHBoxLayout()
    #     account_info_layout = QVBoxLayout()
    #     account_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Aligner à gauche

    #     self.label1 = QLabel("Select Account :")
    #     self.label1.setFont(self.font_manager.get_font("bold", 16))
    #     # layout.addWidget(self.label1)
    #     account_info_layout.addWidget(self.label1)

    #     self.accounts_dropdown = QComboBox()
    #     self.accounts_dropdown.setFixedSize(200, 40)
    #     account_info_layout.addWidget(self.accounts_dropdown)

        

    #     self.account_image = QLabel(self)
    #     self.account_image.setScaledContents(False)   # Ajuste l'image à la taille du QLabel
    #     self.account_image.setGeometry(50, 50, 50, 50)
    #     self.account_image.setFixedSize(70, 70)
    #     apply_rounded_mask(self.account_image, radius=15) 
    #     self.account_image.setScaledContents(True)
    #     self.account_image.setEnabled(False)

    #     account_main_layout.addLayout(account_info_layout)
    #     account_main_layout.addWidget(self.account_image, alignment=Qt.AlignmentFlag.AlignRight)

    #     self.setLayout(account_main_layout)

    #     # layout.addWidget(self.accounts_dropdown)
    #     # layout.addWidget(self.account_image)




    # def add_project_dropdown(self, layout):
    #     """Ajoute le deuxième champ de sélection à la mise en page."""
    #     self.label2 = QLabel("Options disponibles :")
    #     self.label2.setFont(QFont("Arial", 12))
    #     layout.addWidget(self.label2)

    #     self.projects_dropdown = QComboBox()
    #     self.projects_dropdown.setEnabled(False)  # Désactiver initialement
    #     layout.addWidget(self.projects_dropdown)

    # def add_project_info(self, layout):
    #     self.project_image = QLabel(self)
    #     self.project_image.setScaledContents(False)   # Ajuste l'image à la taille du QLabel

    #     self.project_image.setGeometry(50, 50, 50, 50)
    #     self.project_image.setFixedSize(50, 50)
    #     self.project_image.setStyleSheet("""
            
    #     """)
    #     self.project_image.setScaledContents(True)
        
    #     self.project_image.setEnabled(False)
    #     layout.addWidget(self.project_image)



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





class AccountWidget(QWidget):
    def __init__(self,font_manager):
        super().__init__()

        self.font_manager = font_manager
        self.setFont(self.font_manager.get_font("regular", 12))

        self.frame = QFrame(self)
        self.frame.setObjectName("accountFrame")
        self.frame.setFixedSize(320, 90)  # Même taille que AccountWidget
        self.frame.setStyleSheet("""
            QFrame#accountFrame {
                border: 1px solid gray;
                border-radius: 10px;
            }
        """)

        # Layout principal pour l'ensemble des infos Account
        self.account_main_layout = QHBoxLayout(self.frame)  # ⬅️ PAS de self.setLayout() ici
        self.account_main_layout.setContentsMargins(10, 5, 10, 5)  # La méthode setContentsMargins(left, top, right, bottom
        self.account_main_layout.setSpacing(10)


        # Layout vertical pour les infos du compte (label + dropdown)
        account_info_layout = QVBoxLayout()
        account_info_layout.setSpacing(0)
        account_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Aligner à gauche

        # Label pour sélectionner un compte
        self.label1 = QLabel("Selected Account :")
        self.label1.setFont(self.font_manager.get_font("bold", 16))
        account_info_layout.addWidget(self.label1)

        # Dropdown pour choisir un compte
        self.accounts_dropdown = QComboBox()
        self.accounts_dropdown.setFixedSize(200, 40)
        account_info_layout.addWidget(self.accounts_dropdown)
        account_info_layout.addSpacing(20)

        self.add_account_button = QPushButton("Add Account")
        self.add_account_button.setFixedSize(100, self.add_account_button.sizeHint().height())
        account_info_layout.addWidget(self.add_account_button)

        # Ajouter ce layout vertical au layout horizontal
        self.account_main_layout.addLayout(account_info_layout)

        # Ajout de l'image du compte (à droite)
        self.account_image = QLabel(self)
        self.account_image.setFixedSize(70, 70)
        apply_rounded_mask(self.account_image, radius=15) 
        self.account_image.setScaledContents(True)


        # Ajouter l'image à droite
        self.account_main_layout.addWidget(self.account_image, alignment=Qt.AlignmentFlag.AlignRight)
       

    
    def get_layout(self):
        """Retourne le layout pour être ajouté ailleurs"""
        return self.frame

class ProjectWidget(QWidget):
    def __init__(self,font_manager):
        super().__init__()

        # 📌 Encapsulation dans un `QFrame`
        self.font_manager = font_manager
        self.frame = QFrame(self)
        self.frame.setFont(self.font_manager.get_font("regular", 12))
        self.frame.setObjectName("projectFrame")
        self.frame.setFixedSize(320, 90)  # Même taille que AccountWidget
        self.frame.setStyleSheet("""
            QFrame#projectFrame {
                border: 1px solid gray;
                border-radius: 10px;
            }
        """)

        # 📌 Layout principal horizontal
        self.project_main_layout = QHBoxLayout(self.frame)
        self.project_main_layout.setContentsMargins(10, 5, 10, 5)  # Marges internes
        self.project_main_layout.setSpacing(10)  # Espacement entre éléments

        # 📌 Layout vertical pour les infos du projet (label + dropdown)
        project_info_layout = QVBoxLayout()
        project_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Aligner à gauche

        # 📌 Label pour sélectionner un projet
        self.label2 = QLabel("Selected project :")
        self.label2.setFont(self.font_manager.get_font("bold", 16))
        project_info_layout.addWidget(self.label2)

        # 📌 Dropdown pour choisir un projet
        self.projects_dropdown = QComboBox()
        self.projects_dropdown.setFixedSize(200, 40)
        self.projects_dropdown.setEnabled(False)  # Désactivé initialement
        self.projects_dropdown.setEditable(True)  #  Permet de centrer le texte
        self.projects_dropdown.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)  #  Centre le texte
        self.projects_dropdown.setEditable(False)
        project_info_layout.addWidget(self.projects_dropdown)

        project_info_layout.addSpacing(20)

        self.add_project_button = QPushButton("Add Project")
        self.add_project_button.setFixedSize(100, self.add_project_button.sizeHint().height())
        project_info_layout.addWidget(self.add_project_button)
        self.add_project_button.setEnabled(False)
        # self.add_project_button.clicked.connect(self.open_add_project_window)

        # 📌 Ajouter le layout vertical dans le layout horizontal
        self.project_main_layout.addLayout(project_info_layout)

        # 📌 Ajout de l'image du projet (à droite)
        self.project_image = QLabel(self)
        self.project_image.setFixedSize(70, 70)
        apply_rounded_mask(self.project_image, radius=15)
        self.project_image.setScaledContents(True)
        self.project_image.setEnabled(False)

        # 📌 Ajouter l'image à droite
        self.project_main_layout.addWidget(self.project_image, alignment=Qt.AlignmentFlag.AlignRight)

    def get_layout(self):
        """Retourne le `QFrame` pour être ajouté ailleurs"""
        return self.frame  # On retourne `self.frame` au lieu du layout
    
    def open_add_project_window(self,account_id_selected,account_name_selected,controller):
        """Ouvre une nouvelle fenêtre pour ajouter un projet"""
        print("Bouton cliqué !")
        dialog = AddProjectDialog(account_id_selected,account_name_selected,controller,self.font_manager)
        dialog.exec()  #  Affiche la boîte de dialogue en mode bloquant


class GroupCampaignTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 📌 Création du modèle avec colonnes
        self.model = QStandardItemModel(0, 6)  # 0 lignes, 6 colonnes
        self.model.setHorizontalHeaderLabels(["ID", "Date de création", "Nom du groupe", 
                                              "Nombre de campagnes", "Budget margé", "Budget non margé"])
        
        self.locked_columns = [0, 1, 3]  #  Colonnes verrouillées (ID, Date de création, Nombre de campagnes)
        self.modified_rows = set()  #  Stocke les lignes modifiées

        # 📌 Création du tableau
        self.table = QTableView()
        self.table.setSortingEnabled(True)  #  Active le tri au clic
        self.table.setModel(self.model)
        self.table.setFixedSize(800, 150)

        # 📌 Activer la sélection de toute la ligne
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # 📌 Connecter le signal pour détecter les modifications
        self.model.dataChanged.connect(self.highlight_modified_row)

        # 📌 Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_data(self, data):
        """ Met à jour les données du tableau en gardant les colonnes verrouillées"""
        self.model.removeRows(0, self.model.rowCount())  #  Supprime les anciennes lignes

        for row, values in enumerate(data):
            for col, value in enumerate(values):
                item = QStandardItem(str(value))
                if isinstance(value, int):  #  Permet un tri correct des nombres
                    item.setData(value, Qt.ItemDataRole.EditRole)

                #  Désactiver l'édition pour les colonnes verrouillées
                if col in self.locked_columns:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.model.setItem(row, col, item)

    def highlight_modified_row(self, topLeft, bottomRight, roles):
        """ Met en surbrillance une ligne lorsque des données sont modifiées"""
        if Qt.ItemDataRole.EditRole in roles:
            row = topLeft.row()
            if row not in self.modified_rows:
                self.modified_rows.add(row)  #  Ajouter la ligne aux lignes modifiées
                for col in range(self.model.columnCount()):
                    item = self.model.item(row, col)
                    item.setBackground(Qt.GlobalColor.darkMagenta)  #  Couleur normale pour ligne modifiée
                      #  Texte en noir pour bien voir

                    #  Modifier la couleur si la ligne est sélectionnée
                    self.table.setStyleSheet(f"""
                        QTableView::item:selected {{
                            background-color: #FF8C00;  /*  Orange foncé uniquement pour les lignes modifiées */
                            color: white;
                        }}
                    """)
    def get_layout(self):
        """Retourne le QTableView pour être ajouté ailleurs"""
        return self.table




class AddProjectDialog(QDialog):
    def __init__(self,account_id,account_name,controller,font_manager):
        super().__init__()

        self.controller = controller
        self.account_id = account_id
        self.account_name = account_name

        self.setWindowTitle("Creer un nouveau Projet")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        # 📌 Label et champ pour le nom du projet
        self.label2 = QLabel("Account :")
        self.label22 = QLabel(str(account_name))
        self.label3 = QLabel("- ID Xano:")
        self.label32 = QLabel(str(account_id))

        self.label2.setFont(font_manager.get_font("bold", 14))
        self.label22.setFont(font_manager.get_font("regular", 14))
        self.label3.setFont(font_manager.get_font("bold", 14))
        self.label32.setFont(font_manager.get_font("regular", 14))
        
        self.label4 = QLabel("Nom du projet :")
        self.label4.setFont(font_manager.get_font("bold", 12))
        self.label42 = QLabel()
        self.project_name_input = QLineEdit()
        
        row1_layout = QHBoxLayout()
        row1_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  #  Alignement à gauche
        row1_layout.addWidget(self.label2)
        
        row1_layout.addWidget(self.label22)

        row1_layout.addWidget(self.label3)
        row1_layout.addWidget(self.label32)

        row3_layout = QVBoxLayout()
        row3_layout.addWidget(self.label4)
        row3_layout.addWidget(self.project_name_input)

        row3_layout.addWidget(self.label42)

        

        layout.addLayout(row1_layout)
        layout.addLayout(row3_layout)

        # Bouton pour sélectionner une image
        self.image_button = QPushButton("Charger une image")
        self.image_button.clicked.connect(self.load_image)
        layout.addWidget(self.image_button)

        # Label pour afficher l’aperçu de l’image
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(150, 150)  # Taille de l’aperçu
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet("border: 1px solid gray;")  # Ajouter une bordure
        # Créer un layout centré pour l’image
        image_layout = QHBoxLayout()
        image_layout.addStretch()  # Ajoute un espace flexible à gauche
        image_layout.addWidget(self.image_preview, alignment=Qt.AlignmentFlag.AlignCenter)  # Ajoute l'image centrée
        image_layout.addStretch()  # Ajoute un espace flexible à droite

        layout.addLayout(image_layout)

        self.label5 = QLabel()
        layout.addWidget(self.label5)



   
        


        

        # 📌 Bouton d'ajout
        self.submit_button = QPushButton("Ajouter")
        self.submit_button.clicked.connect(self.post_project)  #  Ferme la fenêtre sur validation
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def load_image(self):
        """Ouvre un QFileDialog pour sélectionner une image et vérifie si elle est carrée"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Images (*.png *.jpg *.jpeg)"])
        file_dialog.setViewMode(QFileDialog.ViewMode.List)

        

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.image_path = selected_files[0]  # Stocke le chemin de l’image
                file_size = os.path.getsize(self.image_path)  # Récupère la taille en octets

                max_size = 2000 * 1024  # 500 KB en octets
                pixmap = QPixmap(self.image_path)
                self.label5.setText("")

                # Vérifie si l'image est bien chargée
                if not pixmap.isNull():
                    width = pixmap.width()
                    height = pixmap.height()

                    if file_size > max_size:
                        self.label5.setText("L'image est trop lourde (max 2 MB).")
                        self.label5.setStyleSheet("color: #FF6464;")
                        self.image_preview.clear()
                        self.image_path = None
                        return

                    # Vérifie que l'image est carrée
                    if width != height:
                        self.label5.setText("L'image doit être carrée.")
                        self.label5.setStyleSheet("color: #FF6464;")
                        self.image_preview.clear()
                        self.image_path = None
                        return

                    # Vérifie que la taille est comprise entre 100x100 et 400x400 px
                    if width < 100 or width > 1000:
                        self.label5.setText("L'image doit être entre 100x100 et 1000x1000 pixels.")
                        self.label5.setStyleSheet("color: #FF6464;")
                        self.image_preview.clear()
                        self.image_path = None
                        return

                    # Si tout est valide, affiche l'image
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                    self.image_preview.setPixmap(scaled_pixmap)
                    self.label5.setText("")  # Efface le message d'erreur
                    
                else:
                    self.label5.setText("Impossible de charger l'image.")
                    self.label5.setStyleSheet("color: #FF6464;")  # Message en rouge
    
    def post_project(self):
        """Vérifie les données et envoie le projet via le contrôleur."""
        project_name = self.project_name_input.text().strip()

        # 📌 Vérification via le contrôleur
        is_valid, error_message = self.controller.validate_project_name(project_name)
        if not is_valid:
            self.label42.setText(error_message)
            self.label42.setStyleSheet("color: #FF6464;")
            return

        # 📌 Envoi des données via le contrôleur
        self.image_path = self.image_path if hasattr(self, 'image_path') and self.image_path else None

        success, message = self.controller.send_project_to_xano(self.account_id, project_name, self.image_path)

        if success:
            QMessageBox.information(self, "Succès", "Projet ajouté avec succès.")
            self.accept()  # Ferme la boîte de dialogue
        else:
            QMessageBox.warning(self, "Erreur", f"Échec de l'ajout du projet : {message}")


    # def post_project(self):
    #     """ Vérifie le texte et envoie les données si valides"""

    #     project_name = self.project_name_input.text().strip()  #  Enlever les espaces inutiles

    #     if not project_name:  # Vérifie si le champ est vide
    #         self.label42.setText("Le champ ne peut pas être vide.")
    #         self.label42.setStyleSheet("color: #FF6464;")  # Affiche en rouge
    #         return

    #     if len(project_name) > 32:  #  Vérifie si le texte dépasse 32 caractères
    #         self.label42.setText("Nom trop long, maximum 32 caractères.")
    #         self.label42.setStyleSheet("color: #FF6464;")  #  Message d'erreur en rouge
    #         return

    #     # 📌 Vérifier si le nom contient uniquement des lettres ou des chiffres
    #     if not re.match(r'^[a-zA-Z0-9 ]+$', project_name):  # Accepte lettres, chiffres et espaces
    #         self.label42.setText("Caractères spéciaux non autorisés.")
    #         self.label42.setStyleSheet("color: #FF6464;")  # Message d'erreur en rouge
    #         return

    #     # 📌 Si le nom est valide, appeler le contrôleur
    #     self.controller.post_new_project(self.account_id, project_name)
    #     self.accept()  #  Fermer la fenêtre après validation





def apply_rounded_mask(label, radius=10):
    """Applique un masque arrondi à un QLabel contenant une image."""
    size = label.size()
    mask = QPixmap(size)
    mask.fill(Qt.GlobalColor.transparent)

    painter = QPainter(mask)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(Qt.GlobalColor.white))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(QRect(0, 0, size.width(), size.height()), radius, radius)
    painter.end()

    label.setMask(mask.createMaskFromColor(Qt.GlobalColor.transparent))
