import requests
import telebot
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert

my_bot = telebot.TeleBot('ТУТ API')

cg = CoinGeckoAPI()

table = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_crypto = types.KeyboardButton('Курс криптовалют')
button_usd = types.KeyboardButton('Курс доллара')
button_calc = types.KeyboardButton('Калькулятор валюты')
button_help = types.KeyboardButton('Помощь')

table.row(button_calc)
table.row(button_crypto, button_usd)
table.row(button_help)

inline_kb_crypto = InlineKeyboardMarkup()
inline_btn_btc = InlineKeyboardButton("Bitcoin", callback_data='button_btc')
inline_btn_eth = InlineKeyboardButton("Ethereum", callback_data='button_etc')
inline_btn_ltc = InlineKeyboardButton("Litecoin", callback_data='button_ltc')
inline_kb_crypto.add(inline_btn_btc).add(inline_btn_eth).add(inline_btn_ltc)

inline_kb_money = InlineKeyboardMarkup()
inline_btn_usd = InlineKeyboardButton("USD", callback_data='button_usd')
inline_btn_rub = InlineKeyboardButton("RUB", callback_data='button_rub')
inline_btn_eur = InlineKeyboardButton("EUR", callback_data='button_eur')
inline_kb_money.add(inline_btn_usd).add(inline_btn_rub).add(inline_btn_eur)


@my_bot.message_handler(commands=['start'])
def welcome(message):
	my_bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.username), reply_markup = table)

@my_bot.message_handler(content_types=['text'])
def main(message):
    if message.text == 'Курс криптовалют': 
        price = cg.get_price(ids='bitcoin,litecoin,ethereum,ripple,cardano,polkadot,stellar,chainlink,binancecoin,eos,monero,tron,nem,okb,tezos,vechain,cosmos', vs_currencies='usd')
        my_bot.send_message(message.chat.id, f"Bitcoin — {price['bitcoin']['usd']:.2f}$"
            + f"\nLitecoin — {price['litecoin']['usd']:.2f}$"
            + f"\nEthereum — {price['ethereum']['usd']:.2f}$"
            + f"\nRipple — {price['ripple']['usd']:.2f}$"
            + f"\nCardano — {price['cardano']['usd']:.2f}$"
            + f"\nPolkadot — {price['polkadot']['usd']:.2f}$"
            + f"\nStellar — {price['stellar']['usd']:.2f}$"
            + f"\nChainlink — {price['chainlink']['usd']:.2f}$"
            + f"\nBinance Coin — {price['binancecoin']['usd']:.2f}$"
            + f"\nEOS — {price['eos']['usd']:.2f}$"
            + f"\nMonero — {price['monero']['usd']:.2f}$"
            + f"\nTRON — {price['tron']['usd']:.2f}$"
            + f"\nNEM (XEM) — {price['nem']['usd']:.2f}$"
            + f"\nOKB (XEM) — {price['okb']['usd']:.2f}$"
            + f"\nTezos (XTZ) — {price['tezos']['usd']:.2f}$"
            + f"\nVeChain (VET) — {price['vechain']['usd']:.2f}$"
            + f"\nCosmos (ATOM) — {price['cosmos']['usd']:.2f}$",
            reply_markup = table)
    elif message.text == 'Помощь': 
        my_bot.send_message(message.chat.id, f"Привет! С помощью этого бота ты сможешь узнать актульную информацию по курсам криптовалют, а также стоимости покупки доллара. При нажатии на «Курс криптовалют» показывается курс актуальных криптовалют. При нажатии «Курс доллара» показывается актуальный курс доллара в разных валютах.", reply_markup = table)
    elif message.text == 'Курс доллара': 
        course = convert(amount=1, to=['RUB', 'EUR', 'UAH', 'JPY', 'GBP', 'CHF'])
        my_bot.send_message(message.chat.id, f"1$ = {course['RUB']:.2f}₽ — рубли"
            + f"\n1$ = {course['EUR']:.2f}€ — евро"
            + f"\n1$ = {course['UAH']:.2f}₴ — гривны"
            + f"\n1$ = {course['JPY']:.2f}¥ — йены"
            + f"\n1$ = {course['GBP']:.2f}£ — фунты"
            + f"\n1$ = {course['CHF']:.2f}₣ — франки", 
            reply_markup = table)
    elif message.text == 'Калькулятор валюты': 
        my_bot.send_message(message.chat.id, "Какую криптовалюту будете покупать?", reply_markup = inline_kb_crypto)
    else:
        my_bot.send_message(message.chat.id, "Введите, пожалуйста, корректную команду.")

@my_bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    global crypto
    global valute
    global masid
    if call.data == "button_btc" or call.data == "button_etc" or call.data == "button_ltc":
        if call.data == "button_btc":
            crypto = "Bitcoin"
        elif call.data == "button_etc":
            crypto = "Ethereum"
        elif call.data == "button_ltc":
            crypto = "Litecoin"
        time.sleep(1)
        my_bot.delete_message(call.message.chat.id, call.message.message_id)
        my_bot.send_message(call.message.chat.id, "Какой валютой будете покупать?", reply_markup = inline_kb_money) 
    
    elif call.data == "button_usd" or call.data == "button_rub" or call.data == "button_eur":
        if call.data == "button_usd":
            valute = "USD"
        elif call.data == "button_rub":
            valute = "RUB"
        elif call.data == "button_eur":
            valute = "EUR"
        time.sleep(1)
        my_bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = my_bot.send_message(call.message.chat.id, "Сколько у Вас этой валюты?")
        masid = msg.message_id
        my_bot.register_next_step_handler(msg, final)

def final(message):
    global crypto
    global masid
    global valute
    n = message.text
    time.sleep(1)
    my_bot.delete_message(message.chat.id, masid)
    my_bot.delete_message(message.chat.id, message.message_id)
    try: 
        price = cg.get_price(ids=f'{crypto.lower()}', vs_currencies=f'{valute.lower()}')
        my_bot.send_message(message.chat.id, f"{n} {valute} = {float(n)/float(price[f'{crypto.lower()}'][f'{valute.lower()}'])} {crypto}", reply_markup = table)
    except:
        my_bot.send_message(message.chat.id, "Некорректные значения, пожалуйста, веедите всё правильно.", reply_markup = table)

my_bot.enable_save_next_step_handlers(delay=2)
my_bot.load_next_step_handlers()
my_bot.polling()
