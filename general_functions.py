import json, re
from config import FILES_ROOT_PATH
from bot import bot
from datetime import datetime
from zoneinfo import ZoneInfo

def read_json(folder, file_name):
    path = folder / file_name

    with open (path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content

def export_json(content, folder, file_name):
    path = folder / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def read_txt(folder, file_name):
    path = folder / file_name
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    return content

def save_txt(content, folder, file_name):
    path = folder / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def actually_date():
    date = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
    return date

def check_period_d_m_y(period: str):
    #Checa se ta no nesse formato exemplo 01/01/2000 - 01/01/2000
    return bool(re.fullmatch(r"\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4}", period))

def check_period_m_y(period: str):
    #Checa se ta no nesse formato exemplo 01/2000
    return bool(re.fullmatch(r"\d{2}/\d{4}", period))

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
    users = read_json(FILES_ROOT_PATH, "allowed_users.json")

    allowed_user = False

    for user in users:
        if user["id"] == user_id:
            allowed_user = True
            break

    if allowed_user is False:
        bot.send_message(message.chat.id, "Você não tem permissão para usar esse bot.")
        
    return allowed_user