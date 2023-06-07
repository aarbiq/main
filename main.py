import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from urllib.parse import urlparse, parse_qs

def start(update, context):
    chat_id = update.message.chat_id
    
    # Запрос уникального номера платформы у пользователя
    context.bot.send_message(chat_id=chat_id, text="Введите уникальный номер платформы:")
    
    # Установка состояния для ожидания ввода номера платформы
    context.user_data['state'] = 'wait_platform_id'

def handle_input(update, context):
    chat_id = update.message.chat_id
    input_text = update.message.text
    
    if context.user_data.get('state') == 'wait_platform_id':
        # Регистрация пользователя с уникальным номером платформы
        register_user(chat_id, input_text)
        
        # Создание ссылки с данными пользователя
        link = create_link(chat_id)
        
        # Отправка ссылки пользователю
        context.bot.send_message(chat_id=chat_id, text=f"Ваша ссылка: {link}")
        
        # Сброс состояния
        del context.user_data['state']
    else:
        # Обработка других команд или сообщений
        handle_data(update, context)

def register_user(chat_id, platform_id):
    # Загрузка данных из файла JSON
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Регистрация нового пользователя
    users[str(chat_id)] = {"platform_id": platform_id}
    
    # Сохранение обновленных данных в файл JSON
    with open("users.json", "w") as file:
        json.dump(users, file)

def create_link(chat_id):
    # Создание ссылки с данными пользователя
    link = f"https://165.227.173.249/data?chat_id={chat_id}&payout={payout}&offer_name={offer_name}&offer_id={offer_id}"
    
    return link

def handle_data(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    
    # Извлечение данных из URL
    parsed_data = urlparse(data)
    parsed_query = parse_qs(parsed_data.query)
    
    # Получение значений параметров
    payout = parsed_query.get('payout', [''])[0]
    offer_name = parsed_query.get('offer_name', [''])[0]
    offer_id = parsed_query.get('offer_id', [''])[0]
    
    # Отправка сообщения с данными пользователю
    message = f"У вас новые апрув 🤑\nВыплата: {payout}\nНазвание оффера: {offer_name}\nID оффера: {offer_id}"
    context.bot.send_message(chat_id=chat_id, text=message)

def get_platform_id(chat_id):
    # Загрузка данных из файла JSON
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Получение уникального номера платформы по chat_id
    user_data = users.get(str(chat_id))
    if user_data:
        return user_data.get("platform_id")
    else:
        return None

def main():
    # Создание пустого файла JSON, если его нет
    #with open("users.json", "w") as file:
        #json.dump({}, file)
    
    # Инициализация бота
    updater = Updater("6078697572:AAEdyv6dpN5levAcu8AOCdykMBfYeMTDP2Q", use_context=True)
    dispatcher = updater.dispatcher
    
    # Регистрация команды старт
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Регистрация обработчика ввода пользователя
    input_handler = MessageHandler(Filters.text, handle_input)
    dispatcher.add_handler(input_handler)
    
    # Регистрация обработчика данных
    data_handler = MessageHandler(Filters.text, handle_data)
    dispatcher.add_handler(data_handler)
    
    # Запуск бота
    updater.start_polling()

if __name__ == '__main__':
    main()
