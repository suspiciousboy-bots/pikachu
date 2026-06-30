import os

class Config:
    # Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    OWNER_NAME = os.environ.get("OWNER_NAME", "⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐")
    OWNER_ID = int(os.environ.get("OWNER_ID", 7790607144))
    
    # Optional
    BOT_NAME = os.environ.get("BOT_NAME", "「Pɪᴋᴀᴄʜᴜ」")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Pikachuu_Robot")
    SESSION_DIR = os.environ.get("SESSION_DIR", "/tmp/userbot_sessions")
    SESSION_STRING = os.environ.get("SESSION_STRING", "")

config = Config()
