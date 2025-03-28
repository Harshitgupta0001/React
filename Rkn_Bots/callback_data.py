#The repo is fully coded and modified by @Dypixx.
#Please do not sell or remove credits.

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Script import txt

home_buttons = [[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('About', callback_data='about')
        ],[
        InlineKeyboardButton('Movies ɢʀᴏᴜᴘ 💕', url='https://t.me/moviesworldsupportzone')
        ]] 

about_buttons = [[
        InlineKeyboardButton('🙂 𝐎𝐖𝐍𝐄𝐑', url='https://t.me/Harshit_contact_bot')
        ],[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('🦋 𝙷ome', callback_data='back')
        ],[
        InlineKeyboardButton('📜 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/HGBOTZ_support'),
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/hgbotz')
        ]] 

@Client.on_callback_query()
async def callback_query_handler(client, query: CallbackQuery):
    if query.data == "help":
        await query.message.edit_text(
            txt.HELP_TXT, 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Back', callback_data='back'),
                        InlineKeyboardButton('About', callback_data='about')
                    ]
                ]
            )
        )

    
    elif query.data == "about":
        await query.message.edit_text(
            txt.ABOUT_TXT, 
            reply_markup=InlineKeyboardMarkup(about_buttons))

    
    elif query.data == "back":
        await query.message.edit_text(
            txt.START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(home_buttons))
    
    elif query.data == "close":
        await query.answer("Tʜᴀɴᴋs ғᴏʀ ᴄʟᴏsɪɴɢ ❤️", show_alert=True)
        await query.message.delete()
