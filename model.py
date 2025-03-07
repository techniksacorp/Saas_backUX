import time

class DatabaseModel:
    def __init__(self):
        self.connection = self.initialize_connection()

    def initialize_connection(self):
        """Initialise la connexion à la base de données."""
        # Simuler l'initialisation de la connexion
        time.sleep(1)
        return "Connexion simulée"

    def fetch_secondary_options(self, primary_id):
        """Simule une requête en base pour récupérer les options du second champ."""
        data = {
            1: [(101, "Option A1"), (102, "Option A2")],
            2: [(201, "Option B1"), (202, "Option B2")],
            3: [(301, "Option C1"), (302, "Option C2")],
        }
        return data.get(primary_id, [])

    def send_form_data(self, client, option):
        """Simule l'envoi des données du formulaire à la base de données."""
        # Simuler un délai pour l'envoi des données
        time.sleep(1)
        # Simuler une réussite de l'envoi des données
        return True

