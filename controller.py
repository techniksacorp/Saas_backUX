from model import DatabaseModel
import time

class DataController:
    def __init__(self, ui):
        self.ui = ui  # Référence à l'interface
        self.model = DatabaseModel()  # Initialiser le modèle de base de données

    def load_initial_options(self):
        """Charge les options initiales pour le premier champ de sélection."""

        # Simuler un délai pour le chargement des options initiales
        time.sleep(2)
        initial_data = [
            (1, "Client A"),
            (2, "Client B"),
            (3, "Client C"),
        ]
        for item_id, name in initial_data:
            self.ui.dropdown1.addItem(name, item_id)

        # Masquer l'indicateur de chargement après le chargement des options
        self.ui.hide_loading_indicator()

    def update_secondary_options(self):
        """Met à jour le deuxième champ en fonction de la sélection du premier."""
        selected_id = self.ui.dropdown1.currentData()
        self.ui.dropdown2.setEnabled(bool(selected_id))  # Activer/désactiver le deuxième champ

        if selected_id:
            new_options = self.model.fetch_secondary_options(selected_id)

            # Nettoyer et mettre à jour le deuxième menu
            self.ui.dropdown2.clear()
            for item_id, name in new_options:
                self.ui.dropdown2.addItem(name, item_id)
        else:
            self.ui.dropdown2.clear()

    def send_form_data_to_db(self, client, option):
        """Envoie les données du formulaire à la base de données."""
        success = self.model.send_form_data(client, option)
        if success:
            self.ui.show_message("Succès", "Les données ont été envoyées avec succès.")
        else:
            self.ui.show_message("Erreur", "Échec de l'envoi des données.")
