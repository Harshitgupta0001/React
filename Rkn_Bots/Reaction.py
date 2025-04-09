import requests
from pyrogram import Client, filters, errors, types
from config import Rkn_Bots, AUTH_CHANNEL
import asyncio, re, time, sys, random
from .database import total_user, getid, delete, addCap, updateCap, insert, chnl_ids
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from utils import react_msg 
from Script import script


buttons = [[
        InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ"),
        InlineKeyboardButton('✨ 𝙲𝙾𝙽𝚃𝙰𝙲𝚃 ✨', url="https://t.me/Harshit_contact_bot")
    ],[
        InlineKeyboardButton('〄 Add to me group 〄', url="https://t.me/Reaction_99bot?startgroup=botstart")
    ],[
        InlineKeyboardButton('ˣ 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ˣ', url='https://t.me/Reaction_99bot?startchannel&admin=post_messages+edit_messages+delete_messages'),
    ],[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('🦋 𝙰𝙱𝙾𝚄𝚃', callback_data='about')
    ]]

group_buttons = [[InlineKeyboardButton('✇ Click To Start Me ✇', url="http://t.me/Reaction_99bot?start=True")
               ],[
                  InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ")
                ]] 


back_button = [[
                 InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/HGBOTZ_support'),
                 InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/hgbotz')
              ],[
                 InlineKeyboardButton('🔙 back', callback_data='back')
              ]]

about_buttons = [[
        InlineKeyboardButton('🙂 𝐎𝐖𝐍𝐄𝐑', url='https://t.me/Harshit_contact_bot')
        ],[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('🦋 𝙷𝙾𝙼𝙴', callback_data='back')
        ],[
        InlineKeyboardButton('📜 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/HGBOTZ_support'),
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/hgbotz')
        ]]


async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join {chat.title}', url=chat.invite_link)])
        except Exception as e:
            pass
    return btn

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN)  & filters.command(["stats"]))
async def all_db_users_here(client, message):
    start_t = time.time()
    rkn = await message.reply_text("Processing...")
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
    total_users = await total_user()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rkn.edit(text=f"**--Bot Processed--** \n\n**Bot Started UpTime:** {uptime} \n**Bot Current Ping:** `{time_taken_s:.3f} ᴍꜱ` \n**All Bot Users:** `{total_users}`")


@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if (message.reply_to_message):
        rkn = await message.reply_text("Bot Processing.\nI am checking all bot users.")
        all_users = await getid()
        tot = await total_user()
        success = 0
        failed = 0
        deactivated = 0
        blocked = 0
        await rkn.edit(f"bot ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ started...")
        async for user in all_users:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated +=1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked +=1
                await delete({"_id": user['_id']})
            except Exception as e:
                failed += 1
                await delete({"_id": user['_id']})
                pass
            try:
                await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
            except FloodWait as e:
                await asyncio.sleep(t.x)
        await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
        
# Restart to cancell all process 
@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    rkn_msg = await b.send_message(text="**🔄 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙴𝚂 𝚂𝚃𝙾𝙿𝙴𝙳. 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶...**", chat_id=m.chat.id)       
    await asyncio.sleep(3)
    await rkn_msg.edit("**✅️ 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙴𝙳. 𝙽𝙾𝚆 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚄𝚂𝙴 𝙼𝙴**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
NOTIFICATION_CHANNEL_ID = -1002346166150
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, message):
    client = bot
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn:
                username = (await client.get_me()).username
                if message.command:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
                else:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
                await message.reply_text(text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join the channel then click on try again button. 😇</b>", reply_markup=InlineKeyboardMarkup(btn))
                return
        except Exception as e:
            print(e)
    user_id = int(message.from_user.id)
    reply_markup=InlineKeyboardMarkup(buttons)
    await insert(user_id)
    notification_text = f"🎉 New user started the bot: {message.from_user.mention} (ID: {user_id})"
    await bot.send_message(NOTIFICATION_CHANNEL_ID, notification_text)
    await message.reply_photo(photo=Rkn_Bots.RKN_PIC,
        caption=script.START_TXT.format(message.from_user.mention),
        has_spoiler=True, 
        reply_markup=reply_markup)

@Client.on_message(filters.command("start") & filters.group)
async def group_start_cmd(bot, message):
    await react_msg(bot, message)
    user_id = int(message.from_user.id)
    reply_markup=InlineKeyboardMarkup(group_buttons)
    await insert(user_id)
    await message.reply_text(text=script.START_TXT.format(message.from_user.mention),
        message_effect_id = 5044134455711629726, 
        reply_markup=reply_markup)


#----------------------Fin.py - - - - - - - - - - - - - - - - 

@Client.on_message(filters.command("dice"))
async def roll_dice(bot, message):
    await bot.send_dice(message.chat.id, "🎲")


@Client.on_message(filters.command("arrow"))                                      
async def roll_arrow(bot, message):
    await bot.send_dice(message.chat.id, "🎯")

@Client.on_message(filters.command("goal"))
async def roll_goal(bot, message):
    await bot.send_dice(message.chat.id, "⚽️")

@Client.on_message(filters.command("luck"))
async def roll_luck(bot, message):
    await bot.send_dice(message.chat.id, "🎰")

@Client.on_message(filters.command("throw"))
async def roll_throw(bot, message):
    await bot.send_dice(message.chat.id, "🏀")

@Client.on_message(filters.command(["bowling", "tenpins"]))
async def roll_bowling(bot, message):
    await bot.send_dice(message.chat.id, "🎳")


@Client.on_callback_query(filters.regex('help'))
async def show_help_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.HELP_TXT, reply_markup=InlineKeyboardMarkup(back_button))

@Client.on_callback_query(filters.regex('back'))
async def back_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.HOME_TXT, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex('about'))
async def about_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()# Acknowledge the callback
    await callback_query.message.edit_text(text=script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup(about_buttons))

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["msg"]))
async def send_message_to_channel(bot, message):
    # Check if the command is used correctly
    if len(message.command) < 4:
        await message.reply_text("**Usage:** /msg <channel_id> <loop_time> <message>")
        return



# Game data storage
games = {}

# Emoji for cells
symbols = {
    "X": "❌",
    "O": "⭕",
    " ": "➖"
}

def render_board(board):
    return [
        [
            InlineKeyboardButton(symbols[board[i * 3 + j]], callback_data=f"move:{i * 3 + j}")
            for j in range(3)
        ] for i in range(3)
    ]

def check_win(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8], # rows
        [0,3,6],[1,4,7],[2,5,8], # columns
        [0,4,8],[2,4,6]          # diagonals
    ]
    for line in wins:
        a, b, c = line
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board:
        return "tie"
    return None

@Client.on_message(filters.command("tictactoe") & filters.group)
async def start_game(client, message: Message):
    if message.reply_to_message:
        player1 = message.from_user
        player2 = message.reply_to_message.from_user
        board = [" "] * 9
        game_id = message.chat.id

        games[game_id] = {
            "board": board,
            "players": [player1.id, player2.id],
            "turn": 0,
            "msg_id": None
        }

        board_markup = InlineKeyboardMarkup(render_board(board))
        msg = await message.reply(f"Tic Tac Toe Game!\n{player1.mention} ❌ vs {player2.mention} ⭕\nTurn: {player1.mention}", reply_markup=board_markup)
        games[game_id]["msg_id"] = msg.message_id
    else:
        await message.reply("Reply to someone to start a game!")

@Client.on_callback_query(filters.regex("move"))
async def handle_move(client, callback_query: CallbackQuery):
    data = callback_query.data.split(":")
    index = int(data[1])
    chat_id = callback_query.message.chat.id
    game = games.get(chat_id)

    if not game:
        await callback_query.answer("No game running!")
        return

    board = game["board"]
    user_id = callback_query.from_user.id
    turn = game["turn"]
    player1, player2 = game["players"]

    if user_id != game["players"][turn]:
        await callback_query.answer("Not your turn!", show_alert=False)
        player_mention = (await client.get_users(game["players"][turn])).mention
        await callback_query.message.edit_text(
            f"**Tic Tac Toe Game**\nIt's {player_mention}'s turn!",
            reply_markup=InlineKeyboardMarkup(render_board(board))
        )
        return

    if board[index] != " ":
        await callback_query.answer("Cell already taken!", show_alert=False)
        return

    board[index] = "X" if turn == 0 else "O"
    winner = check_win(board)

    if winner:
        del games[chat_id]
        board_markup = InlineKeyboardMarkup(render_board(board))
        if winner == "tie":
            await callback_query.message.edit_text(
                "Match Drawn!\nNo one wins.",
                reply_markup=board_markup
            )
        else:
            winner_id = player1 if winner == "X" else player2
            winner_mention = (await client.get_users(winner_id)).mention
            await callback_query.message.edit_text(
                f"Game Over!\nWinner: {winner_mention}",
                reply_markup=board_markup
            )
        await callback_query.message.reply(
            "Game finished! Want a rematch?",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("♻️ Rematch", callback_data="rematch")
            ]])
        )
    else:
        game["turn"] = 1 - turn
        player_mention = (await client.get_users(game["players"][game["turn"]])).mention
        await callback_query.message.edit_text(
            f"Tic Tac Toe Game!\nTurn: {player_mention}",
            reply_markup=InlineKeyboardMarkup(render_board(board))
        )

@Client.on_callback_query(filters.regex("rematch"))
async def rematch_game(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    player1 = callback_query.from_user
    previous_game = callback_query.message.reply_to_message

    if not previous_game:
        await callback_query.answer("Can't start rematch.", show_alert=True)
        return

    # Attempt to extract both players from previous board message
    lines = previous_game.text.splitlines()
    try:
        p1_mention = lines[1].split(" vs ")[0]
        p2_mention = lines[1].split(" vs ")[1]
    except:
        await callback_query.answer("Failed to fetch players.", show_alert=True)
        return

    # You could store players better; here we reuse original player
    # Use callback_query.from_user and previous_game.reply_to_message.from_user
    if previous_game.reply_to_message:
        player2 = previous_game.reply_to_message.from_user
    else:
        await callback_query.answer("Original player not found.", show_alert=True)
        return

    board = [" "] * 9
    game_id = chat_id
    games[game_id] = {
        "board": board,
        "players": [player1.id, player2.id],
        "turn": 0,
        "msg_id": None
    }

    board_markup = InlineKeyboardMarkup(render_board(board))
    msg = await callback_query.message.reply(
        f"Tic Tac Toe Rematch!\n{player1.mention} ❌ vs {player2.mention} ⭕\nTurn: {player1.mention}",
        reply_markup=board_markup
    )
    games[game_id]["msg_id"] = msg.message_id
    await callback_query.answer("Rematch started!")


                 

#--------- react.py-------

@Client.on_message(filters.all)
async def send_reaction(bot, message):
    await react_msg(bot, message)
