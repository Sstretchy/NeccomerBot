import telebot
import config
import requests
from telebot import types

bot = telebot.TeleBot(config.token)



@bot.message_handler(commands=["start", "Start", "help", "Help", "привет", "Привет"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, {name}, меня зовут NecommerBOT!'
    ' Введите ИНН некоммерческой организации, которая вас интересует.'.format(name=message.chat.first_name))



@bot.message_handler(content_types=['text'])
def inn(message):
    global inn
    inn = message.text

    if len(inn) != 10 or not inn.isdigit():
        bot.reply_to(message, "Неправильный ввод ИНН, попробуйте снова.")
    else:

        file = requests.get("http://openngo.ru/api/organizations/?inn=" + inn).json()

        try:

            regionname = file['results'][0]['region']['name']
            regioncode = file['results'][0]['region']['code']
            typename = file['results'][0]['type']['name']
            typecode = file['results'][0]['type']['code']
            name = file['results'][0]['name']
            active = file['results'][0]['active']
            inn = file['results'][0]['inn']
            kpp = file['results'][0]['kpp']
            ogrn = file['results'][0]['ogrn']
            money_transfers_sum = file['results'][0]['money_transfers_sum']
            website = file['results'][0]['website']
            contract = file['results'][0]['money_transfers_sum_by_type']['Contract']
            grant = file['results'][0]['money_transfers_sum_by_type']['Grant']
            subsidy = file['results'][0]['money_transfers_sum_by_type']['Subsidy']

            list = [regioncode, regionname, typename, typecode, name, active, inn, kpp, ogrn, money_transfers_sum,
                    contract, grant, subsidy, website]

            for i in range(len(list)):
                list[i] = str(list[i])
                if list[i] == 'True':
                    list[i] = ' действует'
                elif list[i] == 'False':
                    list[i] = ' не действует'
                elif list[i] == 'None':
                    list[i] = 'нет данных'

            bot.send_message(message.chat.id, 'Регион, код региона: \n'+ list[1]+', '+ list[0]+
                                              '\n\nТип и код: '+ list[2]+', '+ list[3]+
                                              '\n\nНаименование: '+list[4]+
                                              '\n\nСтатус: '+list[5]+
                                              '\n\nИНН: '+list[6]+
                                              '\nКПП: '+list[7]+
                                              '\nОГРН: '+list[8]+
                                              '\n\nОбщая сумма финансирования: '+ list[9]+'  рублей'+
                                              '\n\nКонтракты: '+list[10]+'  рублей'+
                                              '\nГранты: ' +list[11]+'  рублей'+
                                              '\nСубсидии: '+ list[12]+'  рублей'+
                                              '\n\nВебсайт: '+ list[13]+
                                              '\n\nСсылка на карточку организации: openngo.ru/organization/'+list[8]+'/')

            knop(message)

        except:
            bot.send_message(message.chat.id, 'Неправильно введен ИНН или организация отсутствует в базе, попробуйте еще раз.')

def knop(message):
    knopka = types.ReplyKeyboardMarkup(
        resize_keyboard=True)  # мы создаём объект нашей будущей клавиатуры, resize_keyboard=True-позволяет клавиатуре растягиваться на необходимую высоту вместо того, чтобы занимать всё пространство.
    knopka.add(*[types.KeyboardButton(Inform) for Inform in ['Закупки', 'Субсидии', 'Гранты', 'В начало']])
    bot.send_message(message.chat.id, 'Какую информацию вы ещё хотите узнать?',
                     reply_markup=knopka)
    bot.register_next_step_handler(message, inform)

def inform(message):
    if message.text == 'Закупки':
        bot.send_message(message.chat.id,
                         parse_mode="Markdown",
                         text='[Ссылка на закупки](http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString=' + str(inn))
    if message.text == 'Субсидии':
        bot.send_message(message.chat.id, 'dodelat')
        knop(message)
    elif message.text == 'Гранты':
        bot.send_message(message.chat.id, 'tozhe dodelat')
        knop(message)
    elif message.text == 'В начало':
        start(message)





if __name__ == "__main__":
    bot.polling(none_stop=True)


