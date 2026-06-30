import os

# ────═◈═─ PIKACHU BOT CONFIGURATION ─═◈═────
# All variables will be set via Render/Deployer Environment Variables
# DO NOT hardcode values here - use environment variables for security

class Config:
    # ────═◈═─ REQUIRED (Must be set in environment) ─═◈═────
    
    # Bot Token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    # Telegram API credentials from my.telegram.org
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    
    # Owner Information
    OWNER_NAME = os.environ.get("OWNER_NAME", "⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐")
    OWNER_ID = int(os.environ.get("OWNER_ID", 7790607144))
    
    # ────═◈═─ OPTIONAL (Has default values) ─═◈═────
    
    # Bot Display Name
    BOT_NAME = os.environ.get("BOT_NAME", "「Pɪᴋᴀᴄʜᴜ」")
    
    # Bot Username (without @)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Pikachuu_Robot")
    
    # Session Directory (where user sessions are stored)
    SESSION_DIR = os.environ.get("SESSION_DIR", "/tmp/userbot_sessions")
    
    # Telethon String Session (Optional - for pre-login)
    SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Create config instance
config = Config()

# ────═◈═─ VALIDATION ─═◈═────
# Check if required variables are set
if not config.BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set! Please set it in environment variables.")
    print("   Get from @BotFather")

if config.API_ID == 0:
    print("❌ ERROR: API_ID is not set! Please set it in environment variables.")
    print("   Get from my.telegram.org")

if not config.API_HASH:
    print("❌ ERROR: API_HASH is not set! Please set it in environment variables.")
    print("   Get from my.telegram.org")

if config.OWNER_ID == 0:
    print("❌ ERROR: OWNER_ID is not set! Please set it in environment variables.")
    print("   Get from @userinfobot")

# ────═◈═─ DISPLAY CONFIGURATION ─═◈═────
print("╔══════════════════════════════════════════════╗")
print("║      ⚡ PIKACHU BOT CONFIGURATION ⚡        ║")
print("╠══════════════════════════════════════════════╣")
print(f"║ 🤖 Bot Name:    {config.BOT_NAME:30}║")
print(f"║ 📌 Bot User:    @{config.BOT_USERNAME:29}║")
print(f"║ 👑 Owner:       {config.OWNER_NAME:30}║")
print(f"║ 🆔 Owner ID:    {str(config.OWNER_ID):30}║")
print(f"║ 🔑 API ID:      {str(config.API_ID):30}║")
print(f"║ 📁 Session Dir: {config.SESSION_DIR[:28]:30}║")
print(f"║ 🔐 Session Str: {'✅ SET' if config.SESSION_STRING else '❌ NOT SET':30}║")
print(f"║ 🟢 Status:      {'✅ CONFIGURED' if config.BOT_TOKEN else '❌ MISSING':30}║")
print("╚══════════════════════════════════════════════╝")
