from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 

button_help = KeyboardButton('/help')
button_info = KeyboardButton('/info')
button_info = KeyboardButton('/stop')

kb_help = ReplyKeyboardMarkup()
kb_help.add(button_help)
kb_help.add(button_info)