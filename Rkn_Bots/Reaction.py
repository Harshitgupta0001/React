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



# Game storage: key = game_id (message.id)
games = {}

# Generate game board
def generate_board(board, game_id, include_quit=True):
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            index = i * 3 + j
            cell = board[index]
            if cell == " ":
                row.append(InlineKeyboardButton("➖", callback_data=f"move|{game_id}|{index}"))
            else:
                row.append(InlineKeyboardButton(cell, callback_data="ignore"))
        buttons.append(row)
    if include_quit:
        buttons.append([InlineKeyboardButton("❌ Quit", callback_data=f"quit|{game_id}")])
    return InlineKeyboardMarkup(buttons)

# Check winner or tie
def check_winner(board):
    combos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for x, y, z in combos:
        if board[x] == board[y] == board[z] and board[x] != " ":
            return board[x]
    if " " not in board:
        return "tie"
    return None

def best_move(board):
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif " " not in board:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

# Timeout logic
async def start_timeout(client, game_id, timeout=60):
    await asyncio.sleep(timeout)
    game = games.get(game_id)
    if game and not game.get("winner"):
        turn = game["turn"]
        opponent_id = game["player_o"] if turn == game["player_x"] else game["player_x"]
        try:
            opponent = await client.get_users(opponent_id)
            msg = f"**Timeout!** <a href='tg://user?id={turn}'>Player</a> took too long.\n**Winner:** {opponent.mention}"
        except:
            msg = "**Timeout!** Player took too long.\nOpponent wins!"
        await game["message"].edit_text(msg)
        games.pop(game_id, None)

# Start game
@Client.on_message(filters.command("tictactoe"))
async def start_game(client, message: Message):
    user1 = message.from_user.id
    chat_id = message.chat.id
    board = [" "] * 9
    game_id = message.id

    if message.chat.type == "private" or len(message.command) == 1:
        games[game_id] = {
            "chat_id": chat_id, "player_x": user1, "player_o": 0,
            "turn": user1, "vs_bot": True, "board": board
        }
        sent = await message.reply(
            f"**You vs Bot**\n**Turn:** {message.from_user.mention}",
            reply_markup=generate_board(board, game_id)
        )
        games[game_id]["message"] = sent
        asyncio.create_task(start_timeout(client, game_id))

    elif len(message.command) == 2:
    try:
        user2 = (await client.get_users(message.command[1])).id
        if user1 == user2:
            return await message.reply("You can't play with yourself.")

        import uuid
        game_id = uuid.uuid4().hex
        board = [" "] * 9

        games[game_id] = {
            "chat_id": chat_id,
            "player_x": user1,
            "player_o": user2,
            "turn": user1,
            "vs_bot": False,
            "board": board,
            "status": "pending"
        }

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Accept", callback_data=f"accept|{game_id}"),
                InlineKeyboardButton("❌ Decline", callback_data=f"decline|{game_id}")
            ]
        ])

        await message.reply(
            f"{message.command[1]}, you’ve been challenged by {message.from_user.mention} to a game of **Tic Tac Toe**!",
            reply_markup=keyboard
        )
    except Exception:
        await message.reply("Invalid username or user not found.") 
# Handle move
@Client.on_callback_query(filters.regex("^move"))
async def handle_move(client, cb: CallbackQuery):
    _, game_id, index = cb.data.split("|")
    game_id = int(game_id)
    index = int(index)
    user_id = cb.from_user.id

    game = games.get(game_id)
    if not game:
        return await cb.answer("Game not found or expired.", show_alert=True)

    board = game["board"]
    turn = game["turn"]
    player_x = game["player_x"]
    player_o = game["player_o"]
    is_bot = game["vs_bot"]

    if turn != user_id:
        return await cb.answer("Not your turn!", show_alert=True)

    if board[index] != " ":
        return await cb.answer("Already taken!", show_alert=True)

    mark = "X" if user_id == player_x else "O"
    board[index] = mark

    winner = check_winner(board)
    if winner:
        game["winner"] = True
        if winner == "tie":
            text = "**Match Draw!**"
        elif is_bot and winner == "O":
            text = "**Bot wins!**"
        else:
            text = f"**Winner:** {cb.from_user.mention}"
        await cb.message.edit_text(text)
        games.pop(game_id, None)
        return

    if is_bot:
        game["turn"] = 0
        bot_move = best_move(board)
        board[bot_move] = "O"
        winner = check_winner(board)
        if winner:
            text = "**Match Draw!**" if winner == "tie" else "**Bot wins!**"
            await cb.message.edit_text(text)
            games.pop(game_id, None)
            return
        game["turn"] = player_x
    else:
        game["turn"] = player_o if turn == player_x else player_x

    turn_user = "Bot" if is_bot and game["turn"] == 0 else (await client.get_users(game["turn"])).mention
    await cb.message.edit_text(
        f"**Turn:** {turn_user}",
        reply_markup=generate_board(board, game_id)
    )
    asyncio.create_task(start_timeout(client, game_id))

#acceot or decline 

@Client.on_callback_query(filters.regex("^accept"))
async def handle_accept(client, cb: CallbackQuery):
    _, challenge_id = cb.data.split("|")
    game = games.get(challenge_id)
    
    if not game:
        return await cb.answer("Challenge not found.", show_alert=True)
    if cb.from_user.id != game["player_o"]:
        return await cb.answer("This challenge is not for you.", show_alert=True)

    # Start the game
    board = [" "] * 9
    game.update({
        "board": board,
        "turn": game["player_x"],
        "vs_bot": False,
        "status": "ongoing"
    })

    await cb.message.edit(
        f"{cb.from_user.mention} accepted the challenge!\n\n**Turn:** {(await client.get_users(game['turn'])).mention}",
        reply_markup=generate_board(board, challenge_id)
    )

@Client.on_callback_query(filters.regex("^decline"))
async def handle_decline(client, cb: CallbackQuery):
    _, challenge_id = cb.data.split("|")
    game = games.pop(challenge_id, None)

    if not game:
        return await cb.answer("Challenge not found.", show_alert=True)
    if cb.from_user.id != game["player_o"]:
        return await cb.answer("This challenge is not for you.", show_alert=True)

    await cb.message.edit(f"{cb.from_user.mention} declined the challenge.")

# Quit game
@Client.on_callback_query(filters.regex("^quit"))
async def quit_game(client, cb: CallbackQuery):
    _, game_id = cb.data.split("|")
    game_id = int(game_id)
    user_id = cb.from_user.id

    game = games.get(game_id)
    if not game:
        return await cb.answer("Game not found or expired.", show_alert=True)

    player_x = game["player_x"]
    player_o = game["player_o"]

    if user_id != player_x and user_id != player_o:
        return await cb.answer("You're not part of this game.", show_alert=True)

    opponent_id = player_o if user_id == player_x else player_x
    try:
        opponent = await client.get_users(opponent_id)
        text = f"**{cb.from_user.mention} quit the game!**\n**Winner:** {opponent.mention}"
    except:
        text = f"**{cb.from_user.mention} quit the game!**\nOpponent wins!"

    await cb.message.edit_text(text)
    games.pop(game_id, None)

# Ignore filler
@Client.on_callback_query(filters.regex("^ignore"))
async def ignore(cb: CallbackQuery):
    await cb.answer()

                 

#--------- react.py-------

@Client.on_message(filters.all)
async def send_reaction(bot, message):
    await react_msg(bot, message)
