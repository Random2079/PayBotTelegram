help_message = '''
Отправьте команду /buy, чтобы перейти к покупке.
Узнать правила можно воспользовавшись командой /terms.
'''

start_message = '''
Здравствуйте! Вас приветствует компания "MicroWife"''' + help_message

terms = '''\
Правила!
'''

item_title = 'Микроволновка'
item_description = '''\
Ремонт и Покупка Б/У
'''

AU_error = '''\
В данную страну доставка не оформляется. Сорри
'''

successful_payment = '''
Платеж на сумму `{total_amount} {currency}` совершен успешно!
'''


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'terms': terms,
    'item_title': item_title,
    'item_description': item_description,
    'AU_error': AU_error,
    'successful_payment': successful_payment,
}
