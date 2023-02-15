from sre_parse import CATEGORIES
from typing import Dict, List
import telegram
from amazon_api import search_items
from create_messages import create_item_html
import time
from datetime import datetime
from itertools import chain
import random
from consts import *
import logging

logging.basicConfig(level=logging.INFO)

# ******  Author: Paolo Francioso ********

def is_active() -> bool:
    now = datetime.now().time()
    return MIN_HOUR < now.hour < MAX_HOUR

def send_consecutive_messages(list_of_struct: List[str]) -> None:
    for i in range(NUMBER_OF_MESSAGES):
        row = i - 1
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


# run bot function
def run_bot(bot: telegram.Bot, categories: Dict[str, List[str]]) -> None:
    
    categories=CATEGORIES
    min_result=NUMBER_OF_MESSAGES*2 - 1
    
    # start loop
    while True:
        try:
            items_full = []

            # randomize categories and keywords
            random.shuffle(categories)
            
            # iterate over keywords
            try:
                for category in categories:
                    
                    # shuffle keywords
                    random.shuffle(categories[category])

                    for keyword in categories[category]:
                        # iterate over pages
                        for page in range(1, MAX_PAGE_SEARCH):
                            items = search_items(keyword, category, item_page=page)
                            # api time limit for another http request is 1 second
                            time.sleep(1)
                            items_full.extend(items)
                        
                        raise StopIteration
            except StopIteration: pass           

            logging.info(f'{5 * "*"} Requests Completed {5 * "*"}')

            # shuffling results times
            random.shuffle(items_full)

            # creating html message, you can find more information in create_messages.py
            res = create_item_html(items_full)

            # while we have items in our list
            while len(res) > min_result:

                # if bot is active
                if is_active():
                    try:
                        # Sending two consecutive messages
                        logging.info(f'{5 * "*"} Sending posts to channel {5 * "*"}')
                        res = send_consecutive_messages(res)

                    except Exception as e:
                        logging.info(e)
                        res = res[4:]
                        continue

                    # Sleep for PAUSE_MINUTES
                    time.sleep(60 * PAUSE_MINUTES)

                else:
                    # if bot is not active
                    logging.info(
                        f'{5 * "*"} Inactive Bot, between  {MIN_HOUR}AM and {MAX_HOUR}PM {5 * "*"}'
                    )
                    time.sleep(60 * 5)

        except Exception as e:
            logging.info(e)
            break


if __name__ == "__main__":
    # Create the bot instance
    bot = telegram.Bot(token=TOKEN)
    # running bot
    run_bot(bot=bot, categories=CATEGORIES)
