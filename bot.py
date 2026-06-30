import os
import glob
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User
from config import config

# ────═◈═─ CONFIGURATION FROM CONFIG ─═◈═────
BOT_TOKEN = config.BOT_TOKEN
API_ID = config.API_ID
API_HASH = config.API_HASH
OWNER_NAME = config.OWNER_NAME
OWNER_ID = config.OWNER_ID
BOT_NAME = config.BOT_NAME
BOT_USERNAME = config.BOT_USERNAME
SESSION_DIR = config.SESSION_DIR
SESSION_STRING = config.SESSION_STRING
# ──────────────────────────────────────────────────

# Create session directory if it doesn't exist
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

# Tracks active live login states inside the Bot DM
user_states = {}

# Multi-user profile backup storage maps: { user_id: { first_name, last_name, about, has_photo } }
USER_BACKUPS = {}

# Initialize the main Bot Manager
bot_session_path = os.path.join(SESSION_DIR, "bot_manager_session")
bot = TelegramClient(bot_session_path, API_ID, API_HASH, timeout=30)

# ────═◈═─ PIKACHU BOT MANAGER ─═◈═────
print("╔══════════════════════════════════════════════╗")
print("║      ⚡ PIKACHU BOT MANAGER ⚡              ║")
print(f"║          Bʏ: {OWNER_NAME}           ║")
print("╚══════════════════════════════════════════════╝")
print("•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°")
print("  🔌 Iɴɪᴛɪᴀʟɪᴢɪɴɢ ᴄᴏʀᴇ ᴇɴɢɪɴᴇ...")
print("  ⚡ Lᴏᴀᴅɪɴɢ ᴍᴜʟᴛɪ-ᴜsᴇʀ ᴍᴏᴅᴜʟᴇs...")
print("•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°\n")

# ────═◈═─ BOT HANDLERS ─═◈═────

@bot.on(events.NewMessage(pattern=r"^\/start$"))
async def start_bot(event):
    if not event.is_private:
        return
    user_states[event.sender_id] = {"step": "awaiting_api_id"}
    await event.respond(
        "╔══════════════════════════════════════╗\n"
        "║     ⚡ PIKACHU MULTI-USER DEPLOYER ⚡  ║\n"
        f"║   Bʏ: {OWNER_NAME}            ║\n"
        "╚══════════════════════════════════════╝\n\n"
        "✨ **Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ Pɪᴋᴀᴄʜᴜ Mᴜʟᴛɪ-Uꜱᴇʀ Dᴇᴘʟᴏʏᴇʀ!**\n\n"
        "📌 Oɴᴄᴇ ʟᴏɢɢᴇᴅ ɪɴ ʜᴇʀᴇ, ʏᴏᴜʀ sᴇssɪᴏɴ ɪs sᴀᴠᴇᴅ sᴀғᴇʟʏ.\n"
        "🔄 Rᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ sᴄʀɪᴘᴛ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʙᴏᴏᴛ ᴜᴘ ʏᴏᴜʀ ᴜsᴇʀʙᴏᴛ!\n\n"
        "⚠️ **Rᴇᴍɪɴᴅᴇʀ:** Wʜᴇɴ sᴇɴᴅɪɴɢ ʏᴏᴜʀ ᴄᴏᴅᴇ, ᴛʏᴘᴇ ɪᴛ ᴡɪᴛʜ sᴘᴀᴄᴇs/ʜʏᴘʜᴇɴs (ᴇ.ɢ., `1-2-3-4-5`).\n\n"
        "🔑 Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **API ID** ᴛᴏ ʙᴇɢɪɴ."
    )

@bot.on(events.NewMessage)
async def sequence_handler(event):
    if not event.is_private or event.text.startswith("/start"):
        return

    user_id = event.sender_id
    state = user_states.get(user_id)
    if not state:
        return

    current_step = state["step"]

    if current_step == "awaiting_api_id":
        if not event.text.isdigit():
            await event.respond("❌ Iɴᴠᴀʟɪᴅ API ID. Sᴇɴᴅ ɴᴜᴍʙᴇʀs ᴏɴʟʏ.")
            return
        state["api_id"] = int(event.text)
        state["step"] = "awaiting_api_hash"
        await event.respond("🔑 Gᴏᴛ ɪᴛ. Nᴏᴡ sᴇɴᴅ ʏᴏᴜʀ **API HASH**.")

    elif current_step == "awaiting_api_hash":
        state["api_hash"] = event.text.strip()
        state["step"] = "awaiting_phone"
        await event.respond("📱 Nᴏᴡ sᴇɴᴅ ʏᴏᴜʀ **Pʜᴏɴᴇ Nᴜᴍʙᴇʀ** ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ (ᴇ.ɢ., `+1234567890`).")

    elif current_step == "awaiting_phone":
        state["phone"] = event.text.strip()
        await event.respond("⏳ *Cᴏɴɴᴇᴄᴛɪɴɢ ᴀɴᴅ ʀᴇǫᴜᴇsᴛɪɴɢ ʏᴏᴜʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴄᴏᴅᴇ...*")
        
        try:
            # Check if SESSION_STRING is available
            if SESSION_STRING:
                # Use string session
                user_client = TelegramClient(StringSession(SESSION_STRING), state["api_id"], state["api_hash"])
                await user_client.connect()
                
                if await user_client.is_user_authorized():
                    await event.respond("✅ Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴡɪᴛʜ sᴛʀɪɴɢ sᴇssɪᴏɴ! Aᴄᴛɪᴠᴀᴛɪɴɢ ᴜsᴇʀʙᴏᴛ...")
                    asyncio.create_task(run_userbot_commands(user_client, user_id))
                    del user_states[user_id]
                    return
                else:
                    await event.respond("❌ Sᴛʀɪɴɢ sᴇssɪᴏɴ ɪs ɴᴏᴛ ᴠᴀʟɪᴅ. Pʟᴇᴀsᴇ ʟᴏɢɪɴ ᴡɪᴛʜ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ.")
                    
            # Use file session (default)
            session_name = f"active_{state['api_id']}_{state['api_hash']}_{user_id}.session"
            user_session_path = os.path.join(SESSION_DIR, session_name)
            user_client = TelegramClient(user_session_path, state["api_id"], state["api_hash"])
            
            await user_client.connect()
            state["client"] = user_client
            
            if await user_client.is_user_authorized():
                await event.respond("✅ Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ! Aᴄᴛɪᴠᴀᴛɪɴɢ ᴜsᴇʀʙᴏᴛ...")
                asyncio.create_task(run_userbot_commands(user_client, user_id))
                del user_states[user_id]
                return
                
            phone_code_hash = await user_client.send_code_request(state["phone"])
            state["phone_code_hash"] = phone_code_hash.phone_code_hash
            state["step"] = "awaiting_code"
            
            await event.respond(
                "📨 **Cᴏᴅᴇ sᴇɴᴛ!** Cʜᴇᴄᴋ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs.\n\n"
                "⚠️ **CRITICAL:** Rᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴅᴇ sᴇᴘᴀʀᴀᴛᴇᴅ ʙʏ ʜʏᴘʜᴇɴs (ᴇ.ɢ., `5-4-3-2-1`)."
            )
        except Exception as e:
            await event.respond(f"❌ Cᴏɴɴᴇᴄᴛɪᴏɴ ғᴀɪʟᴇᴅ: `{e}`\nUꜱᴇ /start ᴛᴏ ᴛʀʏ ᴀɢᴀɪɴ.")
            del user_states[user_id]

    elif current_step == "awaiting_code":
        code = event.text.strip().replace(" ", "").replace("-", "").replace(".", "").replace(",", "")
        user_client = state["client"]
        
        await event.respond("⏳ *Sᴜʙᴍɪᴛᴛɪɴɢ ᴄʀᴇᴅᴇɴᴛɪᴀʟs...*")
        try:
            await user_client.sign_in(phone=state["phone"], code=code, phone_code_hash=state["phone_code_hash"])
            await event.respond("🎉 **Sᴜᴄᴄᴇss! Yᴏᴜʀ ᴜsᴇʀʙᴏᴛ ɪs ɴᴏᴡ ᴀᴄᴛɪᴠᴇ.**")
            asyncio.create_task(run_userbot_commands(user_client, user_id))
            del user_states[user_id]
        except SessionPasswordNeededError:
            state["step"] = "awaiting_password"
            await event.respond("🔐 **Tᴡᴏ-Sᴛᴇᴘ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴅᴇᴛᴇᴄᴛᴇᴅ.** Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ 2FA Cʟᴏᴜᴅ ᴘᴀssᴡᴏʀᴅ.")
        except Exception as e:
            await event.respond(f"❌ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ: `{e}`\nUꜱᴇ /start ᴛᴏ ʀᴇᴛʀʏ.")
            del user_states[user_id]

    elif current_step == "awaiting_password":
        password = event.text.strip()
        user_client = state["client"]
        
        await event.respond("⏳ *Vᴇʀɪғʏɪɴɢ ᴄʟᴏᴜᴅ ᴘᴀssᴡᴏʀᴅ...*")
        try:
            await user_client.sign_in(password=password)
            await event.respond("🎉 **Sᴜᴄᴄᴇss! Yᴏᴜʀ ᴜsᴇʀʙᴏᴛ ɪs ɴᴏᴡ ᴀᴄᴛɪᴠᴇ.**")
            asyncio.create_task(run_userbot_commands(user_client, user_id))
            del user_states[user_id]
        except Exception as e:
            await event.respond(f"❌ Iɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ: `{e}`\nUꜱᴇ /start ᴛᴏ ʀᴇsᴛᴀʀᴛ.")
            del user_states[user_id]

# ────═◈═─ USERBOT EXECUTION ─═◈═────

async def run_userbot_commands(user_client, owner_id):
    try:
        me = await user_client.get_me()
        my_id = me.id
        
        print("\n" + "•" * 50)
        print(f"  ⚡ Uꜱᴇʀʙᴏᴛ Sᴘᴀᴡɴᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!")
        print(f"  👤 Aᴄᴄᴏᴜɴᴛ: {me.first_name} (ID: {my_id})")
        print(f"  👑 Bʏ: {OWNER_NAME}")
        print(f"  📢 Uꜱᴇʀʙᴏᴛ ɪs ɴᴏᴡ ʟɪsᴛᴇɴɪɴɢ ғᴏʀ ᴄᴏᴍᴍᴀɴᴅs!")
        print(f"  📦 BACKUP STATUS: {'BACKUP EXISTS' if my_id in USER_BACKUPS else 'NO BACKUP'}")
        print("•" * 50 + "\n")

        # ────═◈═─ COMMAND: .clone ─═◈═────
        @user_client.on(events.NewMessage(outgoing=True, pattern=r"^\.clone(?: |$)"))
        async def clone_user(event):
            print(f"  🔄 .clone command DETECTED from user {my_id}!")
            global USER_BACKUPS
            
            await event.delete()
            status_msg = await event.respond("🔄 *Pʀᴏᴄᴇssɪɴɢ ᴄʟᴏɴᴇ ʀᴇǫᴜᴇsᴛ...*")
            
            target_user = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                target_user = await user_client.get_entity(reply_msg.sender_id)
            else:
                args = event.text.split(maxsplit=1)
                if len(args) > 1:
                    try:
                        target_user = await user_client.get_entity(args[1])
                    except Exception as e:
                        await status_msg.delete()
                        await event.respond(f"❌ *Cᴏᴜʟᴅ ɴᴏᴛ ғɪɴᴅ ᴜsᴇʀ:* {e}")
                        return
                else:
                    await status_msg.delete()
                    await event.respond("❌ *Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ/ID.*")
                    return

            if not isinstance(target_user, User):
                await status_msg.delete()
                await event.respond("❌ *Tᴀʀɢᴇᴛ ᴍᴜsᴛ ʙᴇ ᴀ Uꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ.*")
                return

            # Save current profile as backup before cloning
            try:
                my_full = await user_client(GetFullUserRequest(my_id))
                my_bio = my_full.full_user.about or ""
            except Exception:
                my_bio = ""

            USER_BACKUPS[my_id] = {
                "first_name": me.first_name or "",
                "last_name": me.last_name or "",
                "about": my_bio,
                "has_photo": bool(me.photo)
            }
            print(f"  📦 Backup saved for user {my_id}")

            try:
                target_full = await user_client(GetFullUserRequest(target_user.id))
                target_bio = target_full.full_user.about or ""
            except Exception:
                target_bio = ""

            await user_client(UpdateProfileRequest(
                first_name=target_user.first_name or "",
                last_name=target_user.last_name or "",
                about=target_bio
            ))

            if target_user.photo:
                await status_msg.delete()
                status_msg = await event.respond("🔄 *Cʟᴏɴɪɴɢ ᴘʀᴏғɪʟᴇ ᴘɪᴄᴛᴜʀᴇ...*")
                
                unique_filename = f"target_dp_{my_id}.jpg"
                photo_path = await user_client.download_profile_photo(target_user.id, file=unique_filename)
                if photo_path:
                    file = await user_client.upload_file(photo_path)
                    await user_client(UploadProfilePhotoRequest(file=file))
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
            
            await status_msg.delete()
            await event.respond(f"👤 *Sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ* [{target_user.first_name}](tg://user?id={target_user.id})*!*")
            print(f"  ✅ .clone completed for user {my_id}")

        # ────═◈═─ COMMAND: .reidentify ─═◈═────
        @user_client.on(events.NewMessage(outgoing=True, pattern=r"^\.reidentify$"))
        async def reidentify_user(event):
            print(f"  🔄 .reidentify command DETECTED from user {my_id}!")
            global USER_BACKUPS
            
            await event.delete()
            status_msg = await event.respond("🔄 *Rᴇᴄᴏɴsɪᴅᴇʀɪɴɢ ɪᴅᴇɴᴛɪᴛʏ ʙᴀᴄᴋᴜᴘ...*")
            
            try:
                fresh_me = await user_client.get_me()
                my_full = await user_client(GetFullUserRequest(my_id))
                my_bio = my_full.full_user.about or ""
                
                USER_BACKUPS[my_id] = {
                    "first_name": fresh_me.first_name or "",
                    "last_name": fresh_me.last_name or "",
                    "about": my_bio,
                    "has_photo": bool(fresh_me.photo)
                }
                
                print(f"  ✅ .reidentify completed! Backup updated for user {my_id}")
                await status_msg.delete()
                await event.respond("✅ *Yᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʟᴏᴏᴋ ʜᴀs ʙᴇᴇɴ sᴀᴠᴇᴅ ᴀs ʙᴀᴄᴋᴜᴘ!*")
            except Exception as e:
                print(f"  ❌ .reidentify failed: {e}")
                await status_msg.delete()
                await event.respond(f"❌ *Fᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ ʙᴀᴄᴋᴜᴘ:* {e}")

        # ────═◈═─ COMMAND: .return ─═◈═────
        @user_client.on(events.NewMessage(outgoing=True, pattern=r"^\.return$"))
        async def restore_user(event):
            print(f"  🔄 .return command DETECTED from user {my_id}!")
            global USER_BACKUPS
            
            await event.delete()
            
            if my_id not in USER_BACKUPS:
                print(f"  ❌ .return failed: No backup found for user {my_id}")
                await event.respond("❌ *Nᴏ ʙᴀᴄᴋᴜᴘ ɪᴅᴇɴᴛɪᴛʏ ᴘʀᴏғɪʟᴇ ғᴏᴜɴᴅ.*")
                return

            status_msg = await event.respond("🔄 *Rᴇsᴛᴏʀɪɴɢ ʏᴏᴜʀ ᴏʀɪɢɪɴᴀʟ ɪᴅᴇɴᴛɪᴛʏ...*")
            backup = USER_BACKUPS[my_id]
            print(f"  📋 Restoring backup for user {my_id}")

            try:
                await user_client(UpdateProfileRequest(
                    first_name=backup["first_name"],
                    last_name=backup["last_name"],
                    about=backup["about"]
                ))
                
                if backup["has_photo"]:
                    try:
                        async for photo in user_client.iter_profile_photos("me"):
                            await user_client(DeletePhotosRequest(id=[photo]))
                            break 
                    except Exception as e:
                        print(f"  ⚠️ Could not delete photo: {e}")
                
                print(f"  ✅ .return completed successfully for user {my_id}!")
                await status_msg.delete()
                await event.respond("✅ *Iᴅᴇɴᴛɪᴛʏ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴛᴏʀᴇᴅ!*")
            except Exception as e:
                print(f"  ❌ .return failed: {e}")
                await status_msg.delete()
                await event.respond(f"⚠️ *Fᴀɪʟᴇᴅ ᴛᴏ ʀᴇsᴛᴏʀᴇ ᴘʀᴏғɪʟᴇ:* {e}")

        # ────═◈═─ COMMAND: .test ─═◈═────
        @user_client.on(events.NewMessage(outgoing=True, pattern=r"^\.test$"))
        async def test_command(event):
            print(f"  ✅ .test command received from user {my_id}")
            await event.edit(f"✅ Uꜱᴇʀʙᴏᴛ ɪs ᴡᴏʀᴋɪɴɢ!\n\n📦 Backup: {'✅ Yes' if my_id in USER_BACKUPS else '❌ No'}\n👤 User ID: {my_id}")

        await user_client.run_until_disconnected()
    except Exception as e:
        print(f"\n⚠️ Uꜱᴇʀʙᴏᴛ sᴇssɪᴏɴ ᴇɴᴅᴇᴅ ғᴏʀ ᴏᴡɴᴇʀ {owner_id}")
        print(f"📝 Eʀʀᴏʀ: {e}\n")

# ────═◈═─ SESSION RESTORATION ─═◈═────

async def auto_load_saved_sessions():
    await asyncio.sleep(2)
    search_pattern = os.path.join(SESSION_DIR, "active_*_*_*.session")
    session_files = glob.glob(search_pattern)
    
    print("\n" + "═" * 50)
    print("  🔍 Sᴄᴀɴɴɪɴɢ ғᴏʀ sᴀᴠᴇᴅ sᴇssɪᴏɴs...")
    print("═" * 50)
    
    if not session_files:
        print("  💡 Nᴏ sᴀᴠᴇᴅ sᴇssɪᴏɴs ғᴏᴜɴᴅ.")
        print("  📩 Aᴡᴀɪᴛɪɴɢ ɴᴇᴡ ᴄᴏɴɴᴇᴄᴛɪᴏɴs ᴠɪᴀ /start")
        print("═" * 50 + "\n")
        return

    print(f"  📂 Fᴏᴜɴᴅ {len(session_files)} sᴀᴠᴇᴅ sᴇssɪᴏɴs")
    print("  🔄 Aᴜᴛᴏ-ᴄᴏɴɴᴇᴄᴛɪɴɢ...")
    print("═" * 50 + "\n")
    
    for path in session_files:
        filename = os.path.basename(path).replace(".session", "")
        parts = filename.split("_")
        if len(parts) >= 4:
            try:
                api_id = int(parts[1])
                api_hash = parts[2]
                owner_id = int(parts[3])
                
                saved_client = TelegramClient(path, api_id, api_hash)
                await saved_client.connect()
                
                if await saved_client.is_user_authorized():
                    asyncio.create_task(run_userbot_commands(saved_client, owner_id))
                else:
                    print(f"  ⚠️ Sᴇssɪᴏɴ ғᴏʀ ᴜsᴇʀ {owner_id} ɪs ɴᴏ ᴠᴀʟɪᴅ")
            except Exception as auto_err:
                print(f"  ❌ Eʀʀᴏʀ ʟᴏᴀᴅɪɴɢ {filename}: {auto_err}")

# ────═◈═─ BOT STARTUP ─═◈═────

print("  🚀 Sᴛᴀʀᴛɪɴɢ ᴛʜᴇ Bᴏᴛ Mᴀɴᴀɢᴇʀ...")
print("  🤖 Cᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ Tᴇʟᴇɢʀᴀᴍ...")

bot.start(bot_token=BOT_TOKEN)
bot.loop.create_task(auto_load_saved_sessions())

print("\n" + "═" * 50)
print("  ⚡ PIKACHU ENGINE ONLINE!")
print(f"  👑 Bʏ: {OWNER_NAME}")
print("  📌 Pᴇʀᴍᴀɴᴇɴᴛ ʀᴇsᴛᴏʀᴀᴛɪᴏɴ ᴀᴄᴛɪᴠᴇ")
print("═" * 50 + "\n")

bot.run_until_disconnected()
