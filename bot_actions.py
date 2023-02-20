from typing import List
import telegram
from telegram.ext import Updater, CommandHandler
from amazon_api import search_item
from create_messages import create_item_html
from consts import *
import logging
import requests
import re

logging.basicConfig(level=logging.INFO)

# ******  Author: Paolo Francioso ********

# baseURL should have https and www before amazon, but we also want to detect URL without it
# Ensure that we can detect all but the baseURL has the correct https URL
baseURL = BASE_URL

if baseURL.startswith("https://www."):
    searchURL = baseURL[12:]
elif baseURL.startswith("http://www."):
    searchURL = baseURL[11:]
    baseURL = "https://www."+searchURL
else:
    searchURL = baseURL
    baseURL = "https://www."+baseURL

#Expand shorted URL (amzn.to links) to normal Amazon URL
def unshortURL(url):
    resp = requests.get("https://"+url)
    return resp.url

def send_consecutive_messages(list_of_struct: List[str], number_of_messages = int) -> None:
    for i in range(number_of_messages):

        pointer_1 = 0 + i * 2
        pointer_2 = 1 + i * 2
        bot.send_message(
            chat_id=CHANNEL_NAME,
            text=list_of_struct[pointer_1],
            reply_markup=list_of_struct[pointer_2],
            parse_mode=telegram.ParseMode.HTML,
        )
    return_counter = pointer_2 + 1    
    return list_of_struct[return_counter:]

def extract_url(text):
     return text.split()[1].strip()

def aff_link_gen(update, context):

    safety_chat_id = str(SAFETY_CHAT_ID)
    if str(update.message.chat.id) == safety_chat_id:

        items_full = []
        pCode = ""
        print('Message Received')
        url = extract_url(update.message.text)
        start = url.find("amzn.to")
        if start!=-1:
            url = unshortURL(url[start:].split()[0])
        start = url.find("amzn.eu")
        if start!=-1:
            url = unshortURL(url[start:].split()[0])
        start = url.find(searchURL)
        if start != -1:
            #Regular expression to extract the product code. Adjust if different URL schemes are found.
            m = re.search(r'(?:dp\/[\w]*)|(?:gp\/product\/[\w]*)',url[start:].split(" ")[0])
            if m != None:
                pCode = m.group(0)
                pCode = pCode[3:]
                print('Product Code: ' + pCode)  
            items = search_item(pCode)
            items_full.extend(items)

            if items_full is not None:
                logging.info(f'{5 * "*"} Requests Completed {5 * "*"}')
                
                # creating html message, you can find more information in create_messages.py
                res = create_item_html(items_full, True)

                try:
                    # Sending two consecutive messages
                    logging.info(f'{5 * "*"} Sending post to channel {5 * "*"}')
                    res = send_consecutive_messages(res, 1)

                except Exception as e:
                    logging.info(e)
                    res = res[2:]
    else:
        bot.send_message(
                chat_id=update.message.chat.id,
                text='Error - Chat ID Not authorized',
                parse_mode=telegram.ParseMode.HTML,
            )



def get_group_id(update, context):
    bot.send_message(
            chat_id=update.message.chat.id,
            text=update.message.chat.id,
            parse_mode=telegram.ParseMode.HTML,
        )

def bot_receiver():

    upd= Updater(TOKEN, use_context=True)
    disp=upd.dispatcher
 
    disp.add_handler(CommandHandler("gen", aff_link_gen))
    disp.add_handler(CommandHandler("gid", get_group_id))
 
    upd.start_polling()
 
    upd.idle()

if __name__ == "__main__":
    # Create the bot instance
    bot = telegram.Bot(token=TOKEN)
    bot_receiver()
