import json
from config import CURRENT_PATH
from bot import bot

def read_json(folder_name, file_name):
    path = CURRENT_PATH / folder_name / file_name

    with open (path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content

def check_user(message):
    """
    Verifica se o usuário está autorizado a utilizar o bot.

    Esta função compara o ID do usuário que enviou a mensagem com uma lista de usuários permitidos. 
    Caso o usuário não esteja autorizado, uma mensagem é enviada informando a falta de permissão.

    Args:
        message (telebot.types.Message): Objeto que contém informações sobre a mensagem recebida.

    Returns:
        bool: Retorna True se o usuário estiver autorizado, False caso contrário.

    Efeito colateral:
        Envia uma mensagem ao usuário caso ele não tenha permissão para usar o bot.
    """
    
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