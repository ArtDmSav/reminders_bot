import configparser
from pathlib import Path

# Absolut path
dir_path = Path.cwd()
path = Path(dir_path, 'config', 'config.ini')
config = configparser.ConfigParser()
config.read(path)

# Constants
BOT_TOKEN = config['Telegram']['bot_token']
BOT_NAME = config['Telegram']['bot_name']
AI_API_KEY = config['Openai']['api_key']
