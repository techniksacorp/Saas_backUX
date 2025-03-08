import time
import requests

class DatabaseModel:
    def __init__(self):
        self.connection = self.initialize_connection()
        self.route_getaccounts = "https://x6ny-u01k-kxvn.p7.xano.io/api:2sk9qabc/account"
        self.route_getprojects = "https://x6ny-u01k-kxvn.p7.xano.io/api:2sk9qabc/project"

    def initialize_connection(self):
        """Initialise la connexion à la base de données."""
        # Simuler l'initialisation de la connexion
        time.sleep(1)
        return "Connexion simulée"
    
    def fetch_accounts(self):
        """Récupère les comptes de la base de données."""
        response = requests.get(self.route_getaccounts)
        # print( response.json() )
        accounts_data = []

        for account in response.json():
            account_logo = account.get('account_logo', {})  # Vérifie si 'account_logo' existe
            account_logo_url = account_logo['url'] if account_logo and 'url' in account_logo else ''

            accounts_data.append((account['id'], account['account_name'], account_logo_url))

        return accounts_data
    
    def fetch_projects(self, account_id):
        """Récupère les comptes de la base de données."""
        data = {
            "account_id": account_id
        }
        response = requests.get(self.route_getprojects, params=data)
        # print( response.json() )
        projects_data = []

        for project in response.json():
            projects_data.append((project['id'], project['Project_Name']))

        return projects_data

        



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

