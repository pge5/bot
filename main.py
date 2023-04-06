import requests 
from aiogram import executor, Dispatcher, Bot  
from bs4 import BeautifulSoup 
import keyboards as kb 


TOKEN = ''  
bot = Bot(token='')
dp = Dispatcher(bot) 
send_or_not = {} 



def parse_sport(country='Россия'):  
    match = requests.get(f'https://news.sportbox.ru/search-content?keys={country}')  
    soup = BeautifulSoup(match.content,
                         'lxml')  
    strongs = soup.find_all('span', {'class': 'text'})  
    strongs = strongs[0:7]  
    strings = [elem.get_text().replace('\xa0', ' ') for elem in
               strongs]  
    out_list = []  
    for i, string in enumerate(strings):
        html_elem = strongs[
            i]  
        link = 'https://news.sportbox.ru/' + html_elem.find_parent().find_parent().find_parent().find('a').get(
            'href') 
        new_soup = BeautifulSoup(requests.get(link).content, 'lxml')  
        more = new_soup.find('p', {'class': 'introduction-block'}) 
        if not more:  
            more = ''
        else:  
            more = more.get_text()  
        out_list.append(f'{string}. {more}([Подробнее]({link}))')  
    out_str = '\n\n'.join(out_list)  
    return out_str  


@dp.message_handler(commands=['start'])  
async def commands(message):
    if message.text == '/start':  
        if message.chat.id in list(
                send_or_not.keys()): 
            if send_or_not[message.chat.id]:  
                await bot.send_message(message.chat.id,
                                       'Бот уже запущен. Пожалуйста, используй команду " /news Страна " ', reply_markup=kb.kb_help)
                return 

        await bot.send_message(message.chat.id,
                               'Привет! Я бот по новостям! Напиши "/news *страна*" и получишь новости этой страны. /stop для остановки работы', reply_markup=kb.kb_help)
        send_or_not[message.chat.id] = True
        return


@dp.message_handler(commands=['stop']) 
async def stop(message):    
    send_or_not[message.chat.id] = False
    await bot.send_message(message.chat.id, 'До скорой встречи!')


@dp.message_handler(commands=['info']) 
async def info(message):
    if message.chat.id in list(
                send_or_not.keys()):
        if send_or_not[message.chat.id]: 

            await bot.send_message(message.chat.id,
                               'Привет! Я бот по новостям! Напиши "/news *страна* " и получишь новости этой страны. /stop для остановки работы', reply_markup=kb.kb_help)


@dp.message_handler(commands=['help']) 
async def help(message):
    if message.chat.id in list(
                send_or_not.keys()): 
        if send_or_not[message.chat.id]: 
            await bot.send_message(message.chat.id,
                           'Все команды бота:\n/start - запуск бота\n/stop - остановка бота\n/info - получить информацию о боте\n/news *страна* - позволяет получить нвоости страны.(Пример: /news Россия)\n/help - открыть все команды бота', reply_markup=kb.kb_help) 


@dp.message_handler(content_types=['text']) 
async def main(message):
    if message.chat.id in list(send_or_not.keys()): 
        if send_or_not[message.chat.id]:  
            if str(message.text).split()[0] != '/news':  
                await bot.send_message(message.chat.id, 'Пожалуйста, используй команду " /news Страна "', reply_markup=kb.kb_help)
                return
            try:
                await bot.send_message(message.chat.id, parse_sport(str(message.text).split()[1]),
                                       parse_mode="Markdown",
                                       disable_web_page_preview=True, reply_markup=kb.kb_help) 
            except: 
                await bot.send_message(message.chat.id, 'Пожалуйста, укажите существующую страну', reply_markup=kb.kb_help)
        else: 
            send_or_not[message.chat.id] = False
            return
    else:  
        send_or_not[message.chat.id] = False
        return


if __name__ == '__main__':  
    executor.start_polling(dp,
             skip_updates=True) 
