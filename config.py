# config.py
# Store all configuration variables here

from dotenv import load_dotenv
load_dotenv()
import os

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
Git_token = os.getenv('Git_token')
Weather_api = os.getenv('Weather_api')
HISTORY_FILE = os.getenv('HISTORY_FILE', 'chat_history.json')
