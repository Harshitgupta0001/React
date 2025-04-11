import requests
from pyrogram import Client, filters, errors, types
from config import Rkn_Bots, AUTH_CHANNEL
import asyncio, re, time, sys, random
from .database import total_user, getid, delete, addCap, updateCap, insert, chnl_ids
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from utils import react_msg 
from Script import script

# In-memory game storage
games = {}

buttons = [[
        InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ"),
        InlineKeyboardButton('🦋 about', callback_data='about')
    ],[
        InlineKeyboardButton('〄 Add to me group 〄', url="https://t.me/Reaction_99bot?startgroup&admin=post_messages+edit_messages+delete_messages")
    ],[
        InlineKeyboardButton('🎮 games', callback_data='games')
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

games_buttons = [[        
        InlineKeyboardButton('🎮 TIC TAC TOE', callback_data='ttt') 
        ],[
        InlineKeyboardButton('🎮 Rock paper scissor', callback_data='sps')
        ],[
        InlineKeyboardButton('More Timepaas 😂', callback_data='dice')
        ],[
        InlineKeyboardButton('🙂 𝐎𝐖𝐍𝐄𝐑', url='https://t.me/Harshit_contact_bot'), 
        InlineKeyboardButton('BACK 🔙', callback_data='back')
        ]]

about_buttons = [[
        InlineKeyboardButton('🙂 𝐎𝐖𝐍𝐄𝐑', url='https://t.me/Harshit_contact_bot')
        ],[
        InlineKeyboardButton('🎮 games', callback_data='games'), 
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


@Client.on_callback_query(filters.regex('games'))
async def games_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.GAMES_TXT, reply_markup=InlineKeyboardMarkup(games_buttons))

@Client.on_callback_query(filters.regex('back'))
async def back_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.HOME_TXT, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex('about'))
async def about_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()# Acknowledge the callback
    await callback_query.message.edit_text(text=script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup(about_buttons))

@Client.on_callback_query(filters.regex('ttt'))
async def ttt_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.TTT_TXT, reply_markup=InlineKeyboardMarkup(back_button))

@Client.on_callback_query(filters.regex('sps'))
async def rps_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.RPS_TXT, reply_markup=InlineKeyboardMarkup(back_button))

@Client.on_callback_query(filters.regex('dice'))
async def dice_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.DICE_TXT, reply_markup=InlineKeyboardMarkup(back_button))


@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["msg"]))
async def send_message_to_channel(bot, message):
    # Check if the command is used correctly
    if len(message.command) < 4:
        await message.reply_text("**Usage:** /msg <channel_id> <loop_time> <message>")
        return



# Optional: store reaction counts per game
reaction_store = {}

async def edit_with_reactions(cb, text, game_id, add_reactions=False):
    if add_reactions:
        reactions = ["❤️", "🥇", "🔥"]
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{emoji} 0", callback_data=f"game_react|{game_id}|{emoji}") for emoji in reactions]]
        )
        await cb.message.edit_text(text, reply_markup=markup)
        reaction_store[game_id] = {emoji: 0 for emoji in reactions}
    else:
        await cb.message.edit_text(text)


@Client.on_callback_query(filters.regex("^game_react"))
async def reaction_handler(client, cb: CallbackQuery):
    _, game_id, emoji = cb.data.split("|")
    game_id = int(game_id)

    if game_id not in reaction_store:
        return await cb.answer("Reaction expired.", show_alert=True)

    reaction_store[game_id][emoji] += 1
    counts = reaction_store[game_id]
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"{e} {counts[e]}", callback_data=f"game_react|{game_id}|{e}") for e in counts]]
    )
    await cb.message.edit_reply_markup(markup)
    await cb.answer("Thanks for reacting!")


# Generate game board
def generate_board(board, game_id, include_quit=True):
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            index = i * 3 + j
            cell = board[index]
            display = {"X": "❌", "O": "⭕", " ": "➖"}[cell]
            if cell == " ":
                row.append(InlineKeyboardButton(display, callback_data=f"move|{game_id}|{index}"))
            else:
                row.append(InlineKeyboardButton(display, callback_data="ignore"))
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

# Timeout logic
async def start_timeout(client, game_id, timeout=60):
    await asyncio.sleep(timeout)
    game = games.get(game_id)
    if game and not game.get("winner") and game.get("status") == "playing":
        turn = game["turn"]
        opponent_id = game["player_o"] if turn == game["player_x"] else game["player_x"]
        try:
            opponent = await client.get_users(opponent_id)
            msg = f"**Timeout!** <a href='tg://user?id={turn}'>Player</a> took too long.\n**Winner:** {opponent.mention}"
        except:
            msg = "**Timeout!** Player took too long.\nOpponent wins!"
        await game["message"].edit_text(msg)
        games.pop(game_id, None)


async def cancel_timeout(game_id):
    if game_id in games:
        games[game_id]["status"] = "ended"

# Bot move
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

# Start game
@Client.on_message(filters.command(["tictactoe", "ttt"]) & filters.all)
async def start_game(client, message: Message):
    if message.sender_chat:
        return await message.reply("Anonymous admins can't play this game. Please switch to your personal account.")

    user1 = message.from_user.id
    chat_id = message.chat.id
    board = [" "] * 9
    game_id = message.id

    # PvBot mode (private or no args)
    if message.chat.type == "private" or (len(message.command) == 1 and not message.reply_to_message):
        games[game_id] = {
            "chat_id": chat_id, "player_x": user1, "player_o": 0,
            "turn": user1, "vs_bot": True, "board": board,
            "status": "playing"
        }
        sent = await message.reply(
            f"**You vs Bot**\n**Turn:** {message.from_user.mention}",
            reply_markup=generate_board(board, game_id)
        )
        games[game_id]["message"] = sent
        asyncio.create_task(start_timeout(client, game_id))

    # PvP mode (via reply or @username)
    elif len(message.command) == 2 or message.reply_to_message:
        try:
            if message.reply_to_message:
                opponent = message.reply_to_message.from_user
            else:
                opponent = await client.get_users(message.command[1])
            user2 = opponent.id

            if user1 == user2:
                return await message.reply("You can't play with yourself.")

            games[game_id] = {
                "chat_id": chat_id,
                "player_x": user1,
                "player_o": user2,
                "status": "pending"
            }

            await message.reply(
                f"{message.from_user.mention} challenged {opponent.mention} to a game of Tic Tac Toe!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Accept", callback_data=f"accept|{game_id}"),
                    InlineKeyboardButton("❌ Decline", callback_data=f"decline|{game_id}")
                ]])
            )
        except Exception:
            await message.reply("Invalid username or user not found.")

    else:
        await message.reply("Usage: `/tictactoe`, `/tictactoe @username`, or reply to a user's message.", quote=True)
# Accept or Decline Challenge
@Client.on_callback_query(filters.regex("^accept|decline"))
async def handle_challenge_response(client, cb: CallbackQuery):
    action, game_id = cb.data.split("|")
    game_id = int(game_id)
    user_id = cb.from_user.id

    game = games.get(game_id)
    if not game or game.get("status") != "pending":
        return await cb.answer("Game not found or already started.", show_alert=True)

    if user_id != game["player_o"]:
        return await cb.answer("Only the challenged player can respond.", show_alert=True)

    if action == "decline":
        await cb.message.edit_text(f"{cb.from_user.mention} declined the game request.")
        games.pop(game_id, None)
        return

    # Accept the challenge
    board = [" "] * 9
    game.update({
        "board": board,
        "turn": game["player_x"],
        "vs_bot": False,
        "status": "playing"
    })

    sent = await cb.message.reply(
        f"{(await client.get_users(game['player_x'])).mention} vs {cb.from_user.mention}\n\n**Turn:** {(await client.get_users(game['player_x'])).mention}",
        reply_markup=generate_board(board, game_id)
    )
    game["message"] = sent
    await cb.message.delete()
    asyncio.create_task(start_timeout(client, game_id))

# Handle Moves
@Client.on_callback_query(filters.regex("^move"))
async def handle_move(client, cb: CallbackQuery):
    _, game_id, index = cb.data.split("|")
    game_id = int(game_id)
    index = int(index)
    user_id = cb.from_user.id

    game = games.get(game_id)
    if not game or game.get("status") != "playing":
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
            text = f"<b>{(await client.get_users(game['player_x'])).mention} vs {(await client.get_users(game['player_o'])).mention}</b>\n\n**<blockquote>LOL 😂 Match Draw!</blockquote>**"
        elif is_bot and winner == "O":
            text = "**Bot wins! 💀**"
        else:
            text = f"**{(await client.get_users(game['player_x'])).mention} vs {(await client.get_users(game['player_o'])).mention}**\n\n<blockquote>WOW Winner 🥇:** {cb.from_user.mention} 🔥</blockquote>"
        await edit_with_reactions(cb, text, game_id, add_reactions=True)
      #  games.pop(game_id, None)
        return

    if is_bot:
        game["turn"] = 0
        bot_move = best_move(board)
        board[bot_move] = "O"
        winner = check_winner(board)
        if winner:
            text = "**LOL 😂 Match Draw!**" if winner == "tie" else f"**Bot wins! 💀 {(await client.get_users(game['player_x'])).mention} Noob 🤡**"
            #await cb.message.edit_text(text)
            #games.pop(game_id, None)
            await edit_with_reactions(cb, text, game_id, add_reactions=True)
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

# Quit Game
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
    await edit_with_reactions(cb, text, game_id, add_reactions=True)
    #await cb.message.edit_text(text)
    #games.pop(game_id, None) 
    await cancel_timeout(game_id)

# Ignore Button
@Client.on_callback_query(filters.regex("^ignore"))
async def ignore(cb: CallbackQuery):
    await cb.answer()



rps_options = ["rock", "paper", "scissors"]
emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

def get_result(p1, p2):
    if p1 == p2:
        return "draw"
    if (p1 == "rock" and p2 == "scissors") or (p1 == "scissors" and p2 == "paper") or (p1 == "paper" and p2 == "rock"):
        return "p1"
    return "p2"

@Client.on_message(filters.command(["rps", "sps"]) & filters.all)
async def rps_start(client, message: Message):
    if message.sender_chat:
        return await message.reply("Anonymous admins can't play this game. Please switch to your personal account.")

    user1 = message.from_user.id
    chat_id = message.chat.id
    game_id = message.id

    if message.chat.type == "private" or (len(message.command) == 1 and not message.reply_to_message):
        games[game_id] = {
            "chat_id": chat_id,
            "player1": user1,
            "player2": "bot",
            "moves": {},
            "mode": "bot"
        }
        await message.reply(
            "**Rock Paper Scissors**\nYou're playing vs Bot.\nChoose your move:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🪨", callback_data=f"rps|{game_id}|rock"),
                 InlineKeyboardButton("📄", callback_data=f"rps|{game_id}|paper"),
                 InlineKeyboardButton("✂️", callback_data=f"rps|{game_id}|scissors")]
            ])
        )

    elif len(message.command) == 2 or message.reply_to_message:
        try:
            if message.reply_to_message:
                opponent = message.reply_to_message.from_user
            else:
                opponent = await client.get_users(message.command[1])

            user2 = opponent.id
            if user1 == user2:
                return await message.reply("You can't challenge yourself.")

            games[game_id] = {
                "chat_id": chat_id,
                "player1": user1,
                "player2": user2,
                "moves": {},
                "mode": "pvp",
                "status": "pending"
            }
            await message.reply(
                f"{message.from_user.mention} challenged {opponent.mention} to a game of Rock Paper Scissors!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Accept", callback_data=f"rps_accept|{game_id}"),
                     InlineKeyboardButton("❌ Decline", callback_data=f"rps_decline|{game_id}")]
                ])
            )
        except:
            await message.reply("User not found.")


@Client.on_callback_query(filters.regex(r"^rps_accept\|"))
async def accept_rps(client, cb: CallbackQuery):
    _, game_id = cb.data.split("|")
    game_id = int(game_id)
    game = games.get(game_id)

    if not game or game["status"] != "pending":
        return await cb.answer("Game not available.", show_alert=True)

    if cb.from_user.id != game["player2"]:
        return await cb.answer("You're not invited to this game!", show_alert=True)

    game["status"] = "active"

    await cb.message.edit_text(
        f"Game started!\nBoth players, choose your moves. In bot pm of u not start the bot 1st start and again challenge ",
        reply_markup=None
    )

    for player in [game["player1"], game["player2"]]:
        try:
            await client.send_message(
                player,
                "Choose your move:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🪨 ", callback_data=f"rps|{game_id}|rock"),
                     InlineKeyboardButton("📄 ", callback_data=f"rps|{game_id}|paper"),
                     InlineKeyboardButton("✂️ ", callback_data=f"rps|{game_id}|scissors")]
                ])
            )
        except:
            pass

@Client.on_callback_query(filters.regex(r"^rps_decline\|"))
async def decline_rps(client, cb: CallbackQuery):
    _, game_id = cb.data.split("|")
    game_id = int(game_id)
    game = games.pop(game_id, None)
    if game:
        await cb.message.edit_text("Challenge declined.")

@Client.on_callback_query(filters.regex(r"^rps\|"))
async def make_move(client, cb: CallbackQuery):
    _, game_id, move = cb.data.split("|")
    game_id = int(game_id)
    user_id = cb.from_user.id
    game = games.get(game_id)

    if not game:
        return await cb.answer("Game expired.", show_alert=True)

    if game["mode"] == "bot":
        if user_id != game["player1"]:
            return await cb.answer("Not your game!", show_alert=True)

        bot_move = random.choice(rps_options)
        result = get_result(move, bot_move)
        user_mention = cb.from_user.mention
        text = f"**You chose:** {emojis[move]}\n\n**Bot chose:** {emojis[bot_move]}\n\n"

        if result == "draw":
            text += "**It's a draw!**"
        elif result == "p1":
            text += f"**{user_mention} wins!**"
        else:
            text += "**Bot wins!**"

        await cb.message.edit_text(text)
        games.pop(game_id, None)

    elif game["mode"] == "pvp":
        if user_id != game["player1"] and user_id != game["player2"]:
            return await cb.answer("Not your game!", show_alert=True)

        if user_id in game["moves"]:
            return await cb.answer("You've already made your move!", show_alert=True)

        game["moves"][user_id] = move
        await cb.answer("Move registered!")

        if len(game["moves"]) == 2:
            p1_id = game["player1"]
            p2_id = game["player2"]
            p1_move = game["moves"][p1_id]
            p2_move = game["moves"][p2_id]
            result = get_result(p1_move, p2_move)

            p1_mention = (await client.get_users(p1_id)).mention
            p2_mention = (await client.get_users(p2_id)).mention

            result_text = f"**{p1_mention} chose:** {emojis[p1_move]}\n**{p2_mention} chose:** {emojis[p2_move]}\n\n"
            if result == "draw":
                result_text += "**It's a draw!**"
            elif result == "p1":
                result_text += f"**Winner:** {p1_mention}"
            else:
                result_text += f"**Winner:** {p2_mention}"

            await client.send_message(game["chat_id"], result_text)

            try:
                await client.send_message(p1_id, result_text)
                await client.send_message(p2_id, result_text)
            except:
                pass

            games.pop(game_id, None)
 

#--------- react.py-------

@Client.on_message(filters.all)
async def send_reaction(bot, message):
    await react_msg(bot, message)
