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

# L'URL de redirection doit correspondre exactement à celle configurée dans la console Google Cloud
# Format : com.adr28.cortexia:/oauth2redirect
REDIRECT_URI = "com.adr28.cortexia:/oauth2redirect"

def get_authorization_url():
    """Génère l'URL d'autorisation Google pour Deep Linking."""
    client_secrets_file = 'client_secret.json'
    if not os.path.exists(client_secrets_file):
        raise FileNotFoundError("Le fichier 'client_secret.json' est manquant.")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, 
        scopes=SCOPES, 
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return auth_url

def exchange_code_for_token(code):
    """Échange le code reçu via le Deep Link contre des credentials."""
    client_secrets_file = 'client_secret.json'
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, 
        scopes=SCOPES, 
        redirect_uri=REDIRECT_URI
    )
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
        
    return json.loads(creds.to_json())

def is_google_connected():
    return os.path.exists('token.json')

def disconnect_google():
    if os.path.exists('token.json'):
        os.remove('token.json')
    return True
