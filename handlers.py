import aiohttp
from telegram import Update
from telegram.ext import CallbackContext

subscribed_users = set()


async def get_currency_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/get_currency') as response:
            data = await response.json()

    return process_currency_data(data)


def process_currency_data(data):
    processed_data = {}

    for currency in data.get("currency", []):
        currency_code = currency.get("currency")
        buy_value = float(currency.get("buy_value", 0))
        sell_value = float(currency.get("sell_value", 0))

        processed_data[currency_code] = {
            "buy_value": buy_value,
            "sell_value": sell_value,
        }

    return processed_data


async def handle_start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id, "Welcome! Use /cur to get tenge buy and sell currency.")


async def handle_buy_price(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    currency_values = await get_currency_data()
    await context.bot.send_message(chat_id, str(currency_values))


async def send_message_to_subscribers(context: CallbackContext):
    for chat_id in subscribed_users:
        currency_values = await get_currency_data()
        await context.bot.send_message(chat_id, str(currency_values))


async def handle_subscribe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    subscribed_users.add(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="You have successfully subscribed to notifications!")
    print(subscribed_users)
