from aiogram import Bot, Dispatcher, types
import logging
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
logging.basicConfig(level=logging.INFO)

API_TOKEN = ******************* #Подставьте свой

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_welcome(message: types.Message):
   await message.reply('Привет!\nПо команде "/order" вы можете выбрать ваш населённый пункт для доставки бетона и оставить свои контактные данные, чтобы мы связались с вами позже\nПо команде "/links" вам будут доступны ссылки\nна наш сайт и группу в ВК, где вы можете узнать больше о нашей компании\nПо команде "/types" вы узнаете о видах бетона\nПо команде "/os" вы можете оставить свой отзыв\nУдачи!') #Так как код работает асинхронно, то обязательно пишем await.

urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Перейти на сайт', url='https://betonrastvorvolhov.ru/')
urlButton2 = InlineKeyboardButton(text='Перейти в группу ВК', url='https://vk.com/betonvolhov')
urlkb.add(urlButton,urlButton2)
 
@dp.message_handler(commands=['links'])
async def url_command(message: types.Message):
   await message.answer('Информационные ссылки, чтобы побольше узнать о нас или задать вопрос:', reply_markup=urlkb)


@dp.message_handler(commands=['types'])
async def send_photo(message: types.Message):
   await message.answer_photo(photo=InputFile('files/types_beton.png'), caption='Виды бетона, предусмотренные нашей лабораторией. Для консультации по выбору определённого вида обратитесь к администратору')

# Define states
class OrderStates(StatesGroup):
    City = State()
    Name = State()
    Phone = State()

# Handler for the /order command
@dp.message_handler(Command("order"))
async def start_order(message: types.Message):
    await message.reply("Давайте начнём оформлять вашу заявку!\nНапишите свой город, пожалуйста")
    await OrderStates.City.set()

# Handler for the city state
@dp.message_handler(state=OrderStates.City)
async def process_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    await message.reply("Как к вам можно обращаться?")
    await OrderStates.Name.set()

# Handler for the name state
@dp.message_handler(state=OrderStates.Name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.reply("Оставьте свой номер телефона для связи")
    await OrderStates.Phone.set()

# Handler for the phone state
@dp.message_handler(state=OrderStates.Phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)

    # Get the user's data from the state
    user_data = await state.get_data()

    # Reset the state
    await state.finish()

    # Send a confirmation message
    await message.reply("Ваша заявка в обработке. Скоро мы с вами свяжемся. Спасибо!")

class OtzuvStates(StatesGroup):
    Otzuv = State()

# Обработка команды /os
@dp.message_handler(commands=['os'])
async def ask_feedback(message: types.Message):
    await message.reply("Пожалуйста, напишите ваш отзыв, обратную связь или что-нибудь приятное С:")
    await OtzuvStates.Otzuv.set()

@dp.message_handler(state=OtzuvStates.Otzuv)
async def process_phone(message: types.Message, state: FSMContext):
    otzuv = message.text
    await state.update_data(otzuv=otzuv)

    # Get the user's data from the state
    user_data = await state.get_data()

    # Reset the state
    await state.finish()

    # Send a confirmation message
    await message.reply("Спасибо за ваш отзыв!")




# # Хранение сообщений
# messages = []

# # Обработка всех входящих сообщений
# @dp.message_handler()
# async def handle_message(message: types.Message):
#     # Добавление сообщения в список
#     messages.append(message.text)

# # Обработка команды /random
# @dp.message_handler(commands=['random'])
# async def send_random_message(message: types.Message):
#     random_message = random.choice(messages)
#     await message.reply(random_message)


# def send_email(subject, message):
#     # Конфигурация SMTP сервера и учетных данных
#     smtp_server = "smtp.yandex.ru"
#     smtp_port = 465
#     smtp_username = "padl1za@yandex.ru"
#     smtp_password = "DaPizda1a"
#     sender_email = "padl1za@yandex.ru"
#     receiver_email = "padl1za@yandex.ru"

#     # Формирование сообщения
#     msg = MIMEMultipart()
#     msg["From"] = sender_email
#     msg["To"] = receiver_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(message, "plain"))

#     # Подключение к SMTP серверу и отправка сообщения
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         server.send_message(msg)

# # Обработка сообщений от пользователя
# def handle_user_message(message):
#     # Получение данных от пользователя
#     city = message["city"]
#     name = message["name"]
#     phone = message["phone"]

#     # Формирование и отправка сообщения на почту администратора
#     subject = "Новая заявка"
#     email_message = f"Город: {city}\nИмя: {name}\nНомер телефона: {phone}"
#     send_email(subject, email_message)

# # Тестирование кода
# user_data = {
#     "city": "Москва",
#     "name": "Иван",
#     "phone": "1234567890"
# }
# handle_user_message(user_data)
    
# Обработка всех остальных сообщений
@dp.message_handler()
async def handle_other_messages(message: types.Message):
    await message.reply("Извините, я не понимаю. Выберите команду из списка /start")

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
