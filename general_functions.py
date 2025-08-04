import json
from config import CURRENT_PATH
from bot import bot

def read_json(folder_name, file_name):
    path = CURRENT_PATH / folder_name / file_name

    with open (path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content

def check_user(message):
    user_id = message.from_user.id
    users = read_json("general_files", "allowed_users.json")

    allowed_user = False

    for user in users:
        if user["id"] == user_id:
            allowed_user = True
            break

    if allowed_user is False:
        bot.send_message(message.chat.id, "Você não tem permissão para usar esse bot.")
        
    return allowed_user