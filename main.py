from telegram.ext import CommandHandler, ApplicationBuilder, CallbackContext
from handlers import handle_start, handle_buy_price, handle_subscribe, send_message_to_subscribers


async def schedule_hourly_job(context: CallbackContext):
    context.job_queue.run_repeating(send_message_to_subscribers, interval=3600, first=0)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6297836283:AAGEaCSnuxlFJmc5a52s09uWJABvsRVAOe8').build()

    start_handler = CommandHandler('start', handle_start)
    cur_handler = CommandHandler('cur', handle_buy_price)
    handle_subscribe_handler = CommandHandler('subscribe', handle_subscribe)

    application.add_handlers([start_handler, cur_handler, handle_subscribe_handler])
    application.job_queue.run_once(schedule_hourly_job, 0)

    application.run_polling()
