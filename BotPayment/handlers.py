from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
from aiogram import types 

from messages import MESSAGES
from config import PAYMENTS_TOKEN, item_url
from main import dp, bot

########### Цены и виды доставок 
PRICE_MICRO = [
    LabeledPrice(label='Консультация', amount=1000 *100),
]
PRICE_FIX_MICRO = [
    LabeledPrice(label='Починка микроволновой печи', amount=1000 *100),
]
PRICE_DIAGNOSTIC = [
    LabeledPrice(label='Вызов и диагностика микроволновки', amount= 500 * 100)
]

DELIVERY_SHIPPING_OPTION = ShippingOption(
    id='superspeed',
    title='Яндекс доставка'
).add(LabeledPrice('Быстро и дешиво', 100*100))

POST_SHIPPING_OPTION = ShippingOption(
    id='post',
    title='Почта России'
)

POST_SHIPPING_OPTION.add(LabeledPrice('О привет налоги НДФЛ 13%', 25*100))
POST_SHIPPING_OPTION.add(LabeledPrice('Хе + на пенсию', 25*100))

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title='Самовывоз'
)
PICKUP_SHIPPING_OPTION.add(LabeledPrice('Самовывоз', 10*100))

###################

# Кнопки и Keyboard

Service = types.KeyboardButton('Услуги')
Company = types.KeyboardButton('О компании')
Support = types.KeyboardButton('Поддержка')

# Кнопки service

back_button = types.KeyboardButton('Назад')
fix_microwife = types.KeyboardButton('Ремонт микроволновки')
diagnostic = types.KeyboardButton('Диагностика')

###################

service = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 3 )
service.add(fix_microwife,diagnostic,back_button)

# Menu

menu = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 3 )
menu.add(Service,Company,Support)

###################

@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
    await message.answer(MESSAGES['start'],reply_markup = menu)

@dp.message_handler()
async def help_cmd(message: Message):
    if message.text == 'Услуги':
        await message.answer(''' С чем вам помочь? 🤔
        Ремонт микроволновки?
        Покупка запчастей от микроволновки?
        Диагностика микроволновки? ''',reply_markup = service)
    elif message.text == 'Диагностика':
        await message.answer(''' Спасибо что выбрали нас!!! ''')
        await bot.send_invoice(message.chat.id,
            title=MESSAGES['item_title'],
            description=MESSAGES['item_description'],
            provider_token=PAYMENTS_TOKEN,
            currency='rub',
            photo_url=fix_microwife,
            photo_height=512,
            photo_width=512,
            photo_size=512,
            need_email=True,
            need_phone_number=True,
            is_flexible=True,
            prices=PRICE_DIAGNOSTIC,
            start_parameter='example',
            payload='some_invoice')
    elif message.text == 'Ремонт микроволновки':
        await message.answer(''' Спасибо что выбрали нас!!! ''')
        await bot.send_invoice(message.chat.id,
            title=MESSAGES['item_title'],
            description=MESSAGES['item_description'],
            provider_token=PAYMENTS_TOKEN,
            currency='rub',
            photo_url=fix_microwife,
            photo_height=512,
            photo_width=512,
            photo_size=512,
            need_email=True,
            need_phone_number=True,
            is_flexible=True,
            prices=PRICE_FIX_MICRO,
            start_parameter='example',
            payload='some_invoice')
    elif message.text == 'Назад':
        await message.answer('''Возращаю обратно (✋🫥👍)''',reply_markup=menu)
    elif message.text == 'О компании':
        await message.answer('Наша компания "MicroWife"M')
    elif message.text == 'Поддержка':
        await message.answer('Поддержка прибудет скоро')
    else:
        await message.answer('Не верные команды! 🤬')

@dp.message_handler(commands=['terms'])
async def terms_cmd(message: Message):
    await message.answer(MESSAGES['terms'])

@dp.message_handler(commands=['buy'])
async def buy_process(message: Message):
    await bot.send_invoice(message.chat.id,
                           title=MESSAGES['item_title'],
                           description=MESSAGES['item_description'],
                           provider_token=PAYMENTS_TOKEN,
                           currency='rub',
                           photo_url=item_url,
                           photo_height=512,
                           photo_width=512,
                           photo_size=512,
                           need_email=True,
                           need_phone_number=True,
                           is_flexible=True,
                           prices=PRICE_MICRO,
                           start_parameter='example',
                           payload='some_invoice')
    
@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    if shipping_query.shipping_address.country_code == 'AU':
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message=MESSAGES['AU_error']
        )

    shipping_options = [DELIVERY_SHIPPING_OPTION]

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(POST_SHIPPING_OPTION)

        if shipping_query.shipping_address.city == 'Сургут':
            shipping_options.append(PICKUP_SHIPPING_OPTION)

    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")

    