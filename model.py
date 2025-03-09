import time
import requests
from datetime import datetime,timezone

class DatabaseModel:
    def __init__(self):
        self.connection = self.initialize_connection()
        self.route_getaccounts = "https://x6ny-u01k-kxvn.p7.xano.io/api:2sk9qabc/account"
        self.route_getprojects = "https://x6ny-u01k-kxvn.p7.xano.io/api:2sk9qabc/project"
        self.route_getgroupcampaigns = "https://x6ny-u01k-kxvn.p7.xano.io/api:2sk9qabc/groupcampaign"

        self.route_postproject = "https://x6ny-u01k-kxvn.p7.xano.io/api:2sk9qabc/post_project"


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
            project_logo = project.get('logo', {})
            project_logo_url = project_logo['url'] if project_logo and 'url' in project_logo else ''
            projects_data.append((project['id'], project['Project_Name'],project_logo_url))
            

        return projects_data
    
    def fetch_groupcampaigns(self, project_id, account_id):
        """Récupère les comptes de la base de données."""
        data = {
            "account_id": account_id,
            "project_id": project_id
        }
        response = requests.get(self.route_getgroupcampaigns, params=data)
        # print( response.json() )
        groupscampaigns_data = []

        for groupcampaigns in response.json():
            groupscampaigns_data.append([
                groupcampaigns['id'],# ID du groupe de campagnes
                datetime.fromtimestamp(groupcampaigns['created_at'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d') , # Date de creation
                groupcampaigns['groupname'],# Nom du groupe
                groupcampaigns['nb_campain'],# Nombre de campagnes
                groupcampaigns['total_budget_margin'],  # Budget total avec marge
                groupcampaigns['total_budget_nomargin'] # Budget total sans marge
            ])
        return groupscampaigns_data
       



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

    def post_project(self, account_id, project_name, logo_path):
        
        # Préparer les données du formulaire
        data = {
            "account_id": account_id,
            "Project_Name": project_name,
            'logo': None
        }
        
        # Vérifier si un logo est fourni
        files = {"image": open(logo_path, "rb")} if logo_path else None
        
        
        try:
            response = requests.post(self.route_postproject, data=data, files=files)
            response_data = response.json()  # Convertir la réponse en JSON
            print(response_data)

            if response.status_code == 200:
                if response_data == "Project name already exist":
                    return False, "Le projet existe déjà."
                print("Projet ajouté avec succès :", response_data)
                return True, response_data
            else:
                print("Erreur :", response_data)
                return False, response_data
            
            

        except Exception as e:
            print("Erreur de connexion :", e)
            return None