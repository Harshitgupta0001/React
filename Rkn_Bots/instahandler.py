#The repo is fully coded and modified by @Dypixx.
#Please do not sell or remove credits.

from pyrogram import Client, filters
import shutil, time, os, instaloader, asyncio
from pyrogram.errors import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from .fsub import get_fsub
from .db import data

user_last_download_time = {}
@Client.on_message(filters.text & filters.private & ~filters.command(['start','ban', 'unban', 'broadcast', 'stats', 'restart'])) 
async def download_instagram_content(client, message):
    if message.text.startswith("/"):return
    if await data.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support", url="https/t.me/HGBOTZ_support")]]))
        return
    if IS_FSUB and not await get_fsub(client, message):return
    try:
        if ENABLE_FLOOD_WAIT:
            current_time = time.time()
            last_download_time = user_last_download_time.get(message.chat.id, 0)
            remaining_time = FLOOD_WAIT_TIME - (current_time - last_download_time)
            if remaining_time > 0:
                T = await message.reply_text("**Pʟᴇᴀsᴇ ᴡᴀɪᴛ...**")
                while remaining_time > 0:
                    minutes, seconds = divmod(int(remaining_time), 60)
                    time_text = f"{minutes}m{seconds}s" if minutes > 0 else f"{seconds}s"
                    try:
                        await T.edit_text(
                            f"**Pʟᴇᴀsᴇ ᴡᴀɪᴛ {time_text} ʙᴇғᴏʀᴇ ᴍᴀᴋɪɴɢ ᴀɴᴏᴛʜᴇʀ ʀᴇǫᴜᴇsᴛ.**"
                        )
                    except Exception as e:
                        print(f"Error updating flood wait text: {e}")
                        break
                    await asyncio.sleep(1)
                    current_time = time.time()
                    remaining_time = FLOOD_WAIT_TIME - (current_time - last_download_time)
                try:
                    await T.edit_text("**Nᴏᴡ ʏᴏᴜ ᴄᴀɴ sᴇɴᴅ ᴍᴇ ᴀɴᴏᴛʜᴇʀ ᴛᴀsᴋ!**")
                except Exception as e:
                    print(f"Error finalizing flood wait text: {e}")
                return
            user_last_download_time[message.chat.id] = current_time
        url = message.text.strip()
        if not url.startswith("https://www.instagram.com/"):
            await message.reply("**Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ ᴘᴏsᴛ/ʀᴇᴇʟ ʟɪɴᴋ...**")
            return
        T = await message.reply("**processing...🔻**") 
        await asyncio.sleep(2)
        await T.edit_text("⏳")
        L = instaloader.Instaloader()
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)
        if "/reel/" in url or "/p/" in url:
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=download_dir)
        else:
            await T.delete()
            await message.reply("**Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ʀᴇᴇʟ ᴏʀ ᴘᴏsᴛ ʟɪɴᴋ.**")
            return
        downloaded_files = os.listdir(download_dir)
        total_photos = 0
        total_videos = 0
        if "/reel/" in url:
            for file in downloaded_files:
                file_path = os.path.join(download_dir, file)
                if file_path.endswith('.mp4'):
                    await client.send_video(
                        chat_id=DUMP_CHANNEL,
                        video=file_path,
                        caption=f"**Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ {message.from_user.mention}\n\nSᴏᴜʀᴄᴇ URL: <a href='{url}'>Cʟɪᴄᴋ Hᴇʀᴇ</a>**"
                    )
                    await message.reply_video(video=file_path, caption="**Tʜᴀɴᴋs Fᴏʀ Usɪɴɢ ᴍᴇ ❤️\n<b><blockquote>𝙿𝚘𝚠𝚎𝚛𝚍 𝙱𝚢 ➥ <a href = 'http://t.me/hgbotz'>🦋 HGBOTZ </a></blockquote></b>**", message_effect_id = 5159385139981059251)
                    os.remove(file_path)
                    total_videos += 1
                else:
                    os.remove(file_path)
        elif "/p/" in url:
            for file in downloaded_files:
                file_path = os.path.join(download_dir, file)
                if file_path.endswith(('.jpg', '.png')):
                    await client.send_photo(
                        chat_id=DUMP_CHANNEL,
                        photo=file_path,
                        caption=f"**Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ {message.from_user.mention}\n\nSᴏᴜʀᴄᴇ URL: <a href='{url}'>Cʟɪᴄᴋ Hᴇʀᴇ</a>**"
                    )
                    await message.reply_photo(photo=file_path, message_effect_id = 5159385139981059251)
                    os.remove(file_path)
                    total_photos += 1
                elif file_path.endswith('.mp4'):
                    os.remove(file_path)
        shutil.rmtree(download_dir)
        await T.delete()
        if total_photos > 0 and total_videos == 0:
            await message.reply(f"**Dᴏᴡɴʟᴏᴀᴅᴇᴅ {total_photos} ᴘʜᴏᴛᴏ's sᴜᴄᴄᴇssғᴜʟʟʏ...**")
        elif total_videos > 0 and total_photos == 0:
            await message.reply(f"**Dᴏᴡɴʟᴏᴀᴅᴇᴅ {total_videos} ᴠɪᴅᴇᴏ's sᴜᴄᴄᴇssғᴜʟʟʏ...**")
        else:
            await message.reply("**Nᴏ ᴠᴀʟɪᴅ ᴄᴏɴᴛᴇɴᴛ ғᴏᴜɴᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ...**")
    except FloodWait as e:
        await message.reply_text(f"Please wait {e.value} seconds and try again.")
    except InputUserDeactivated:
        print(f"User {message.chat.id} is deactivated.")
    except UserIsBlocked:
        print(f"User {message.chat.id} has blocked the bot.")
    except PeerIdInvalid:
        print(f"Bot cannot initiate conversation with {message.chat.id}.")
    except Exception as error:
        print(error)
        await message.reply_text(f"An error occurred: {str(error)}")
