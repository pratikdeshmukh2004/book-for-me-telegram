from telegram import *

from telegram.ext import *
from pprint import pprint
import json


updater = Updater(token="YOUR_TOKEN")

dispatcher = updater.dispatcher

customers = {}

def startCommand(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [
        
        [
            InlineKeyboardButton("š New Search", callback_data="new_search")
        ]
    ]
    context.bot.send_message(
        chat.id,
        "*Hi {} {}! š Welcome to BookForMe bot. Here is what I can:*\n\nā Search for cheapest flights š\nā Track tickets prices š\nā Notify about price changes š\n\nShall we start? š".format(
            chat.first_name, chat.last_name
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def meCommand(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.id not in customers:
        customers[chat.id] = {"a_city": "", "d_city": ""}
    buttons = [
        
        [
            InlineKeyboardButton("š« Change Departure", callback_data="change_d"),
            InlineKeyboardButton("š¬ Change Arrival", callback_data="change_a")
        ]
    ]
    context.bot.send_message(
        chat.id,
        "*Hi {} {}!*\n\nš« Departure City: {}\nš¬ Arrival City: {}\n\nChange city š".format(
            chat.first_name,
            chat.last_name,
            customers[chat.id]['d_city'],
            customers[chat.id]['a_city'],
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    chat = update.effective_chat
    global customers
    update.callback_query.answer()
    if "new_search" in query:
        search_types = [[
            InlineKeyboardButton("One Way", callback_data="one_way"),
            InlineKeyboardButton("Return", callback_data="return"),
        ]]
        context.bot.send_message(chat.id, "Please select the type of search š", reply_markup=InlineKeyboardMarkup(search_types))
    if "one_way" in query:
        msg = context.bot.send_message(
            chat.id,
            "š« Enter the city of departure (e.g.: Nagpur)",
            reply_markup=ForceReply()
        )
        c_id = msg['chat']['id']
        if c_id not in customers:
            customers[c_id] = {"d_city": msg.message_id}
        else:
            customers[c_id]['d_city'] = msg.message_id

def messageHandler(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if update.message.reply_to_message == None:
        print(customers)
    elif update.message.reply_to_message.message_id == customers[chat.id]['d_city']:
        customers[chat.id]['d_city'] = update.message.text
        msg = context.bot.send_message(
            chat.id,
            "š¬ Enter the city of arrival (e.g.: Dharmshala)",
            reply_markup=ForceReply()
        )
        if chat.id not in customers:
            customers[chat.id] = {"a_city": msg.message_id}
        else:
            customers[chat.id]['a_city'] = msg.message_id
    elif update.message.reply_to_message.message_id == customers[chat.id]['a_city']:
        customers[chat.id]['a_city'] = update.message.text
        context.bot.send_message(chat.id, "š Wait. Searching best filghts for you...")


dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(CommandHandler("me", meCommand))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

if __name__ == "__main__":
    print("Running telegram bot...")
    updater.start_polling()