import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Les scopes nécessaires pour Gmail, Calendar et Drive
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

def authenticate_google():
    """
    Gère le flux OAuth2 pour obtenir des credentials Google.
    Retourne les credentials sous forme de dictionnaire pour stockage.
    """
    creds = None
    token_file = 'token.json'
    client_secrets_file = 'client_secret.json'

    # Vérification de la présence du fichier client_secret.json
    if not os.path.exists(client_secrets_file):
        raise FileNotFoundError("Le fichier 'client_secret.json' est manquant. Veuillez le placer à la racine du projet.")

    # On tente de charger des credentials existants
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # Si pas de credentials valides, on lance le flux d'authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            # run_local_server ouvre le navigateur et attend la réponse
            creds = flow.run_local_server(port=0)
        
        # Sauvegarde des credentials pour la prochaine fois
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return json.loads(creds.to_json())

def is_google_connected():
    """Vérifie si l'utilisateur est connecté à Google."""
    return os.path.exists('token.json')

def disconnect_google():
    """Déconnecte l'utilisateur en supprimant le token."""
    if os.path.exists('token.json'):
        os.remove('token.json')
    return True
