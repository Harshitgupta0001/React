# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr

from pyrogram import Client, filters, errors, types
from config import Rkn_Bots, AUTH_CHANNEL
import asyncio, re, time, sys, random, os, json
from .database import total_user, getid, delete, addCap, updateCap, insert, chnl_ids
from pyrogram.errors import *
from pyrogram.types import *
from utils import react_msg 

buttons = [[
        InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ"),
        InlineKeyboardButton('✨ 𝙲𝙾𝙽𝚃𝙰𝙲𝚃 ✨', url="https://t.me/Harshit_contact_bot")
    ],[
        InlineKeyboardButton('〄 Add to me group 〄', url="https://t.me/Reaction_99bot?startgroup=botstart")
    ]]

group_buttons = [[InlineKeyboardButton('✇ Click To Start Me ✇', url="http://t.me/Reaction_99bot?start=True")
             ],[
                  InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ")]] 

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
    await message.reply_photo(photo="https://envs.sh/SQw.jpg",
        caption=f"<b>Hᴇʟʟᴏ 😎 {message.from_user.mention} ✨</b>\n<b><blockquote>ɪ ᴀᴍ SIMPEL 😁 BUT ᴘᴏᴡᴇʀꜰᴜʟʟ AUTO REACTION ʙᴏᴛ ᴊᴜꜱᴛ Make Admin in Your Group/Chat to see Magic☜ </blockquote></b>\n<blockquote expandable>For Fun Use These Commands\n◉ /dice\n◉ /arrow\n◉ /goal\n◉ /luck\n◉ /throw\n◉ /bowling\n◉ /tenpins</blockquote>\n<b><spoiler>🔋Maintained by <a href='https://t.me/Harshit_contact_bot'>ℍ𝕒ℝ𝕤ℍ𝕚𝕋</a></spoiler><b>",
        has_spoiler=True, 
        reply_markup=reply_markup)

@Client.on_message(filters.command("start") & filters.group)
async def group_start_cmd(bot, message):
    await react_msg(bot, message)
    user_id = int(message.from_user.id)
    reply_markup=InlineKeyboardMarkup(group_buttons)
    await insert(user_id)
    await message.reply_text(text=f"<b>Hᴇʟʟᴏ 😎 {message.from_user.mention} ✨</b>\n<b><blockquote>ɪ ᴀᴍ ᴘᴏᴡᴇʀꜰᴜʟʟ AUTO REACTION ʙᴏᴛ ᴊᴜꜱᴛ Make Admin in Your Group/Chat to see Magic☜ </blockquote></b>\n<blockquote expandable>For Fun Use These Commands\n◉ /dice\n◉ /arrow\n◉ /goal\n◉ /luck\n◉ /throw\n◉ /bowling\n◉ /tenpins</blockquote>",
        reply_markup=reply_markup)

#@Client.on_message(filters.all)
#async def send_reaction(bot, message):
#    await react_msg(bot, message)

#---------------------------Fun.py----------------(((((((
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

#---------------------------Tic.py-------------------(((

# Starting the Tic-Tac-Toe game
@Client.on_message(filters.command("tic"))
async def tic_cmnd(client, message):
    chat_id = message.chat.id
    text = "Let's play Tic Tac Toe! You are X, and the bot is O."
    reset_board(chat_id)
    await send_game_board(client, chat_id)


# Reset the board for the given chat_id
def reset_board(chat_id):
    board = ["", "", "", "", "", "", "", "", ""]
    save_board(chat_id, board)


# Save the board state to a file
def save_board(chat_id, board):
    with open(f"board_{chat_id}.json", "w") as f:
        json.dump(board, f)


# Load the board state from a file
def load_board(chat_id):
    if os.path.exists(f"board_{chat_id}.json"):
        with open(f"board_{chat_id}.json", "r") as f:
            return json.load(f)
    else:
        return ["", "", "", "", "", "", "", "", ""]


# Send the Tic-Tac-Toe board as an inline keyboard
async def send_game_board(client, chat_id, message_id=None):
    board = load_board(chat_id)

    keyboard = [
        [
            InlineKeyboardButton(board[0] or ".", callback_data="0"),
            InlineKeyboardButton(board[1] or ".", callback_data="1"),
            InlineKeyboardButton(board[2] or ".", callback_data="2")
        ],
        [
            InlineKeyboardButton(board[3] or ".", callback_data="3"),
            InlineKeyboardButton(board[4] or ".", callback_data="4"),
            InlineKeyboardButton(board[5] or ".", callback_data="5")
        ],
        [
            InlineKeyboardButton(board[6] or ".", callback_data="6"),
            InlineKeyboardButton(board[7] or ".", callback_data="7"),
            InlineKeyboardButton(board[8] or ".", callback_data="8")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id:
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text="Tic Tac Toe", reply_markup=reply_markup)
    else:
        await client.send_message(chat_id=chat_id, text="Tic Tac Toe", reply_markup=reply_markup)


# Handling the player's move
@Client.on_callback_query()
async def handle_move(client, callback_query):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id
    callback_data = callback_query.data
    board = load_board(chat_id)

    if board[int(callback_data)] == "":
        board[int(callback_data)] = "X"

        if check_winner(board, "X"):
            await client.send_message(chat_id=chat_id, text="You win!")
            reset_board(chat_id)
            await send_game_board(client, chat_id, message_id)
            return

        if is_board_full(board):
            await client.send_message(chat_id=chat_id, text="It's a draw!")
            reset_board(chat_id)
            await send_game_board(client, chat_id, message_id)
            return

        board = bot_move(board)

        if check_winner(board, "O"):
            await client.send_message(chat_id=chat_id, text="The bot wins!")
            reset_board(chat_id)
            await send_game_board(client, chat_id, message_id)
            return

        if is_board_full(board):
            await client.send_message(chat_id=chat_id, text="It's a draw!")
            reset_board(chat_id)
            await send_game_board(client, chat_id, message_id)
            return

        save_board(chat_id, board)
        await send_game_board(client, chat_id, message_id)


# Bot's move logic
def bot_move(board):
    winning_move = find_winning_move(board, "O")
    if winning_move is not None:
        board[winning_move] = "O"
        return board

    blocking_move = find_winning_move(board, "X")
    if blocking_move is not None:
        board[blocking_move] = "O"
        return board

    if board[4] == "":
        board[4] = "O"
        return board

    corners = [0, 2, 6, 8]
    for corner in corners:
        if board[corner] == "":
            board[corner] = "O"
            return board

    sides = [1, 3, 5, 7]
    for side in sides:
        if board[side] == "":
            board[side] = "O"
            return board

    return board


# Finding a winning move
def find_winning_move(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for combo in winning_combinations:
        player_count = sum(1 for i in combo if board[i] == player)
        empty_index = next((i for i in combo if board[i] == ""), None)
        if player_count == 2 and empty_index is not None:
            return empty_index

    return None


# Check if a player has won
def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    return any(all(board[i] == player for i in combo) for combo in winning_combinations)


# Check if the board is full
def is_board_full(board):
    return all(cell != "" for cell in board)
