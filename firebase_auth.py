import webview
import requests
import json
import base64
import urllib.parse

# Aquí debes reemplazar con tu configuración
CLIENT_ID = 'TU_CLIENT_ID'
REDIRECT_URI = 'http://localhost'
AUTH_URL = f'https://accounts.google.com/o/oauth2/v2/auth?response_type=token&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=profile%20email'

def get_access_token():
    # Abre una ventana del navegador para la autenticación
    webview.create_window('Autenticación de Google', AUTH_URL)
    webview.start()
    # Después de la autenticación, obtén el token de acceso de la URL
    # Esto es solo un ejemplo. Necesitarás implementar el manejo de la respuesta de redireccionamiento.
    access_token = 'TOKEN_OBTENIDO_DESDE_LA_URL'
    return access_token

def get_user_info(token):
    # Usa el token para obtener información del usuario
    response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={
        'Authorization': f'Bearer {token}'
    })
    return response.json()
