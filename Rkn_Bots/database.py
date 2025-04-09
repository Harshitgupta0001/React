import motor.motor_asyncio
from config import Rkn_Bots

client = motor.motor_asyncio.AsyncIOMotorClient(Rkn_Bots.DB_URL)
db = client[Rkn_Bots.DB_NAME]
chnl_ids = db.chnl_ids
users = db.users

games = db.games  # Create a new collection

async def save_game(game_id, game_data):
    await games.update_one({"_id": game_id}, {"$set": game_data}, upsert=True)

async def get_game(game_id):
    return await games.find_one({"_id": game_id})

async def delete_game(game_id):
    await games.delete_one({"_id": game_id})


#insert user data
async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
# Total User
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users

async def delete(id):
    await users.delete_one(id)
                     
async def addCap(chnl_id, caption):
    dets = {"chnl_id": chnl_id, "caption": caption}
    await chnl_ids.insert_one(dets)

async def updateCap(chnl_id, caption):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$set": {"caption": caption}})

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Bots
# Developer @RknDeveloperr
