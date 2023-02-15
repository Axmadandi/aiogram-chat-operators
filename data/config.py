from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "5686437575:AAHCXDbi-4a9PujtdMlP3rOALwvhe5_gMzs"  # Забираем значение типа str
ADMINS = "5462919277", '771423617'  # Тут у нас будет список из админов
  # Тоже str, но для айпи адреса хоста

support_ids = [
    5462919277,
    771423617
    
    
]
