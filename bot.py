import os
import telebot
from telebot import types

API_TOKEN = 'YOUR_BOT_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

channel_url = "https://t.me/your_channel"

admin_ids = [123456789, 987654321]  # Replace with real admin IDs

users_file = 'users.txt'
languages_file = 'languages.txt'

user_languages = {}

welcome_message = {
    'ru': """
Привет! Я KiKoVPN, твой милый-помощник для безопасного и анонимного интернета! 🌸
Я помогу тебе настроить VPN и обеспечу твою конфиденциальность. Выбери нужный раздел в меню ниже, чтобы начать.
""",
    'en': """
Hello! I'm KiKoVPN, your cute assistant for safe and anonymous internet! 🌸
I'll help you set up a VPN and ensure your privacy. Choose the desired section in the menu below to get started.
"""
}

about_us_text = {
    'ru': """
Мы - команда KiKoVPN, стремимся обеспечить вашу безопасность и анонимность в интернете. Наши услуги помогут вам оставаться защищенными и конфиденциальными.
""",
    'en': """
We are the KiKoVPN team, striving to ensure your safety and anonymity on the internet. Our services will help you stay protected and confidential.
"""
}

privacy_text = {
    'ru': """
Мы не собираем логи и не храним информацию о наших пользователях. Ваша конфиденциальность - наш приоритет!
""",
    'en': """
We do not collect logs or store information about our users. Your privacy is our priority!
"""
}



def main_menu(chat_id):
    language = user_languages.get(chat_id, 'ru')
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("VPN CFG", callback_data="vpn_configs"),
               types.InlineKeyboardButton("О нас" if language == 'ru' else "About Us", callback_data="about_us"),
               types.InlineKeyboardButton("Приватность" if language == 'ru' else "Privacy", callback_data="privacy"),
               types.InlineKeyboardButton("Канал" if language == 'ru' else "Channel", url=channel_url))
    if chat_id in admin_ids:
        markup.add(types.InlineKeyboardButton("Админ панель" if language == 'ru' else "Admin Panel", callback_data="admin_panel"))
    return markup

def list_vpn_configs(chat_id):
    language = user_languages.get(chat_id, 'ru')
    configs = [f for f in os.listdir('.') if f.endswith('.ovpn')]
    markup = types.InlineKeyboardMarkup(row_width=2)
    for config in configs:
        buttons = [types.InlineKeyboardButton(config, callback_data=f"send_{config}")]
        if chat_id in admin_ids:
            buttons.append(types.InlineKeyboardButton("🗑️", callback_data=f"delete_{config}"))
        markup.row(*buttons)
    if chat_id in admin_ids:
        markup.add(types.InlineKeyboardButton("➕", callback_data="add_config"))
    markup.add(types.InlineKeyboardButton("Назад" if language == 'ru' else "Back", callback_data="main_menu"))
    return markup

def admin_panel(chat_id):
    language = user_languages.get(chat_id, 'ru')
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("➕ Админ" if language == 'ru' else "➕ Admin", callback_data="add_admin"),
               types.InlineKeyboardButton("➖ Админ" if language == 'ru' else "➖ Admin", callback_data="remove_admin"),
               types.InlineKeyboardButton("✏️ Канал" if language == 'ru' else "✏️ Channel", callback_data="change_channel_url"),
               types.InlineKeyboardButton("Юзеры" if language == 'ru' else "Users", callback_data="list_users"),
               types.InlineKeyboardButton("Назад" if language == 'ru' else "Back", callback_data="main_menu"))
    return markup

def send_vpn_config(chat_id, config_name):
    with open(config_name, 'rb') as config_file:
        bot.send_document(chat_id, config_file)

def delete_vpn_config(chat_id, config_name):
    if os.path.exists(config_name):
        os.remove(config_name)
        bot.send_message(chat_id, f"Конфигурация {config_name} успешно удалена!" if user_languages.get(chat_id, 'ru') == 'ru' else f"Configuration {config_name} successfully deleted!", reply_markup=main_menu(chat_id))
    else:
        bot.send_message(chat_id, f"Конфигурация {config_name} не найдена." if user_languages.get(chat_id, 'ru') == 'ru' else f"Configuration {config_name} not found.", reply_markup=main_menu(chat_id))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in user_languages:
        bot.send_message(message.chat.id, welcome_message[user_languages[message.chat.id]], reply_markup=main_menu(message.chat.id))
    else:
        language_markup = types.InlineKeyboardMarkup(row_width=2)
        language_markup.add(types.InlineKeyboardButton("English 🇬🇧", callback_data="set_language_en"),
                            types.InlineKeyboardButton("Русский 🇷🇺", callback_data="set_language_ru"))
        bot.send_message(message.chat.id, "Выбери язык\nSelect language", reply_markup=language_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data.startswith("set_language_"):
            language = call.data.split("_")[-1]
            user_languages[call.message.chat.id] = language
            save_language(call.message.chat.id, language)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome_message[language], reply_markup=main_menu(call.message.chat.id))
        elif call.data == "vpn_configs":
            new_text = "Выберите VPN-конфигурацию:" if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Choose a VPN configuration:"
            new_markup = list_vpn_configs(call.message.chat.id)
            if call.message.text != new_text or call.message.reply_markup != new_markup:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=new_markup)
        elif call.data.startswith("send_"):
            config_name = call.data[5:]
            send_vpn_config(call.message.chat.id, config_name)
        elif call.data.startswith("delete_"):
            if call.message.chat.id in admin_ids:
                config_name = call.data[7:]
                delete_vpn_config(call.message.chat.id, config_name)
            else:
                bot.answer_callback_query(call.id, "Только администраторы могут удалять конфигурации." if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Only administrators can delete configurations.")
        elif call.data == "about_us":
            text = about_us_text[user_languages.get(call.message.chat.id, 'ru')]
            if call.message.text != text:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=back_button(call.message.chat.id))
        elif call.data == "privacy":
            text = privacy_text[user_languages.get(call.message.chat.id, 'ru')]
            if call.message.text != text:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=back_button(call.message.chat.id))
        elif call.data == "add_config":
            if call.message.chat.id in admin_ids:
                new_text = "Отправьте файл конфигурации для добавления." if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Send the configuration file to add."
                if call.message.text != new_text:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=back_button(call.message.chat.id))
            else:
                bot.answer_callback_query(call.id, "Только администраторы могут добавлять конфигурации." if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Only administrators can add configurations.")
        elif call.data == "admin_panel":
            new_text = "Админ панель:" if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Admin Panel:"
            new_markup = admin_panel(call.message.chat.id)
            if call.message.text != new_text or call.message.reply_markup != new_markup:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=new_markup)
        elif call.data == "add_admin":
            new_text = "Отправьте ID пользователя для добавления в администраторы." if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Send the user ID to add as an administrator."
            if call.message.text != new_text:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=back_button(call.message.chat.id))
        elif call.data == "remove_admin":
            new_text = "Отправьте ID пользователя для удаления из администраторов." if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Send the user ID to remove from administrators."
            if call.message.text != new_text:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=back_button(call.message.chat.id))
        elif call.data == "change_channel_url":
            new_text = "Отправьте новую ссылку на телеграм канал." if user_languages.get(call.message.chat.id, 'ru') == 'ru' else "Send the new Telegram channel link."
            if call.message.text != new_text:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=back_button(call.message.chat.id))
        elif call.data == "list_users":
            users = get_users()
            bot.send_message(call.message.chat.id, f"Пользователи: {', '.join(users)}" if user_languages.get(call.message.chat.id, 'ru') == 'ru' else f"Users: {', '.join(users)}", reply_markup=admin_panel(call.message.chat.id))
        elif call.data == "main_menu":
            if call.message.text != welcome_message[user_languages.get(call.message.chat.id, 'ru')]:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome_message[user_languages.get(call.message.chat.id, 'ru')], reply_markup=main_menu(call.message.chat.id))
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.id in admin_ids:
        if message.reply_to_message:
            if message.text.isdigit():
                user_id = int(message.text)
                if "добавления в администраторы" in message.reply_to_message.text or "add as an administrator" in message.reply_to_message.text:
                    if user_id not in admin_ids:
                        admin_ids.append(user_id)
                        bot.reply_to(message, f"Пользователь {user_id} добавлен в администраторы." if user_languages.get(message.chat.id, 'ru') == 'ru' else f"User {user_id} added as an administrator.", reply_markup=main_menu(message.chat.id))
                    else:
                        bot.reply_to(message, f"Пользователь {user_id} уже является администратором." if user_languages.get(message.chat.id, 'ru') == 'ru' else f"User {user_id} is already an administrator.", reply_markup=main_menu(message.chat.id))
                elif "удаления из администраторов" in message.reply_to_message.text or "remove from administrators" in message.reply_to_message.text:
                    if user_id in admin_ids:
                        admin_ids.remove(user_id)
                        bot.reply_to(message, f"Пользователь {user_id} удален из администраторов." if user_languages.get(message.chat.id, 'ru') == 'ru' else f"User {user_id} removed from administrators.", reply_markup=main_menu(message.chat.id))
                    else:
                        bot.reply_to(message, f"Пользователь {user_id} не является администратором." if user_languages.get(message.chat.id, 'ru') == 'ru' else f"User {user_id} is not an administrator.", reply_markup=main_menu(message.chat.id))
            elif "новую ссылку на телеграм канал" in message.reply_to_message.text or "new Telegram channel link" in message.reply_to_message.text:
                global channel_url
                channel_url = message.text
                bot.reply_to(message, f"Ссылка на телеграм канал изменена на {channel_url}." if user_languages.get(message.chat.id, 'ru') == 'ru' else f"Telegram channel link changed to {channel_url}.", reply_markup=main_menu(message.chat.id))

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.file_name.endswith('.ovpn'):
        if message.chat.id in admin_ids:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(message.document.file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Конфигурация успешно добавлена!" if user_languages.get(message.chat.id, 'ru') == 'ru' else "Configuration successfully added!", reply_markup=main_menu(message.chat.id))
        else:
            bot.reply_to(message, "Только администраторы могут добавлять конфигурации." if user_languages.get(message.chat.id, 'ru') == 'ru' else "Only administrators can add configurations.", reply_markup=back_button(message.chat.id))
    else:
        bot.reply_to(message, "Пожалуйста, отправьте файл конфигурации .ovpn." if user_languages.get(message.chat.id, 'ru') == 'ru' else "Please send a .ovpn configuration file.", reply_markup=back_button(message.chat.id))

def add_user(user_id):
    if not os.path.exists(users_file):
        with open(users_file, 'w') as file:
            file.write(str(user_id))
    else:
        with open(users_file, 'r') as file:
            users = file.read().split(',')
        if str(user_id) not in users:
            users.append(str(user_id))
            with open(users_file, 'w') as file:
                file.write(','.join(users))

def get_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            users = file.read().split(',')
        return users
    return []

def save_language(user_id, language):
    user_languages[user_id] = language
    with open(languages_file, 'a') as file:
        file.write(f"{user_id},{language}\n")

def load_languages():
    if os.path.exists(languages_file):
        with open(languages_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                user_id, language = line.strip().split(',')
                user_languages[int(user_id)] = language

def back_button(chat_id):
    language = user_languages.get(chat_id, 'ru')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад" if language == 'ru' else "Back", callback_data="main_menu"))
    return markup

load_languages()
bot.polling()
