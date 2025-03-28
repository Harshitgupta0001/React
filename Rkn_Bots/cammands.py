#The repo is fully coded and modified by @Dypixx.
#Please do not sell or remove credits.

from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
import time
import asyncio
from Script import txt
from .db import data
from .fsub import get_fsub

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):
    if await data.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support", url="https://t.me/HGBOTZ_support")]]))
        return
    if await data.get_user(message.from_user.id) is None:
        await data.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, text="#NEw_USer\n\nUser: {}\nID: {}".format(message.from_user.mention, message.from_user.id))
    if IS_FSUB and not await get_fsub(client, message):return
    await message.reply_photo(photo="https://i.ibb.co/8g4M7s6W/photo-2025-03-06-10-31-33-7478642289837867024.jpg", 
        caption = txt.START_TXT.format(message.from_user.mention),
        message_effect_id = 5104841245755180586, 
        has_spoiler = True, 
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❗️ʜᴇʟᴘ", callback_data="help"), InlineKeyboardButton("About", callback_data="about")
            ],[
             InlineKeyboardButton("Movie Group 🎉", url="https://t.me/moviesworldsupportzone") 
            ]
        ])
    )

@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN))
async def broadcasting_func(client: Client, message: Message):
    try:
        msg = await message.reply_text("Wait a second!")
        if not message.reply_to_message:
            return await msg.edit("<b>Please reply to a message to broadcast.</b>")
        await msg.edit("Processing ...")
        completed = 0
        failed = 0
        to_copy_msg = message.reply_to_message
        users_list = await data.get_all_users()
        
        for i, userDoc in enumerate(users_list):
            if i % 20 == 0:
                await msg.edit(f"Total: {i}\nCompleted: {completed}\nFailed: {failed}")
            user_id = userDoc.get("user_id")
            if not user_id:
                continue
            try:
                await to_copy_msg.copy(int(user_id))
                completed += 1
                await asyncio.sleep(0.1)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await to_copy_msg.copy(int(user_id))
                    completed += 1
                except Exception:
                    failed += 1
            except Exception as e:
                print(f"Error in broadcasting to {user_id}: {e}")
                failed += 1
                
        await msg.edit(f"Successfully Broadcasted\nTotal: {len(users_list)}\nCompleted: {completed}\nFailed: {failed}")
    except Exception as e:
        print(f"Error in broadcast: {e}")
        await message.reply_text("An error occurred while broadcasting.")

@Client.on_message(filters.command("ban") & filters.private & filters.user(ADMIN))
async def ban_user_cmd(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Usage: /ban user_id")
            return
        user_id = int(command_parts[1])
        reason = " ".join(command_parts[2:]) if len(command_parts) > 2 else None
        try:
            user = await client.get_users(user_id)
        except Exception:
            await message.reply_text("Unable to find user.")
            return
        if await data.ban_user(user_id, reason):
            ban_message = f"User {user.mention} has been banned."
            if reason:
                ban_message += f"\nReason: {reason}"
            await message.reply_text(ban_message)
        else:
            await message.reply_text("Failed to ban user.")
    except ValueError:
        await message.reply_text("Please provide a valid user ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("unban") & filters.private & filters.user(ADMIN))
async def unban_user_cmd(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Usage: /unban user_id")
            return
        user_id = int(command_parts[1])
        try:
            user = await client.get_users(user_id)
        except Exception:
            await message.reply_text("Unable to find user.")
            return
        if await data.unban_user(user_id):
            await message.reply_text(f"User {user.mention} has been unbanned.")
        else:
            await message.reply_text("Failed to unban user or user was not banned.")
    except ValueError:
        await message.reply_text("Please provide a valid user ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
