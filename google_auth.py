import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from flask import session

# Config Google OAuth
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/analytics.readonly"]

# Inicializa o fluxo OAuth2
def iniciar_fluxo():
    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    session['flow'] = flow
    return auth_url

# Troca o código por credenciais e salva na sessão
def trocar_codigo_por_credenciais(code):
    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    session['credentials'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
