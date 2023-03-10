#from sre_parse import CATEGORIES
from typing import Dict, List
import telegram
from amazon_api import search_items
from create_messages import create_item_html
import time
from datetime import datetime
import random
from consts import *
import logging

logging.basicConfig(level=logging.INFO)

# ******  Author: Paolo Francioso ********

def is_active() -> bool:
    now = datetime.now().time()
    return MIN_HOUR < now.hour < MAX_HOUR

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

# run bot function
def run_bot(bot: telegram.Bot, categories: Dict[str, List[str]]) -> None:
    
    min_result=NUMBER_OF_MESSAGES*2 - 1
    res_except=NUMBER_OF_MESSAGES*2
    
    # start loop
    while True:
        try:
            items_full = []

            # randomize categories and keywords
            randomizer = len(categories) - 1
            random_array = random.randint(0, randomizer)
            
            counter = 0
            # iterate over keywords
            try:
                for category in categories:
                    if counter == random_array:
                        
                        # shuffle keywords
                        random.shuffle(categories[category])

                        for keyword in categories[category]:
                            # iterate over pages
                            for page in range(1, MAX_PAGE_SEARCH):
                                items = search_items(keyword, category, item_page=page)
                                # api time limit for another http request is 1 second
                                time.sleep(1)
                                if items is not None:
                                    items_full.extend(items)
                            
                            raise StopIteration
                    counter = counter + 1

            except StopIteration: pass           

            logging.info(f'{5 * "*"} Requests Completed {5 * "*"}')

            # shuffling results times
            random.shuffle(items_full)

            # creating html message, you can find more information in create_messages.py
            res = create_item_html(items_full, False)

            # while we have items in our list
            while len(res) > min_result:

                # if bot is active
                if is_active():
                    try:
                        # Sending two consecutive messages
                        logging.info(f'{5 * "*"} Sending posts to channel {5 * "*"}')
                        res = send_consecutive_messages(res, NUMBER_OF_MESSAGES)

                    except Exception as e:
                        logging.info(e)
                        res = res[res_except:]
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
    run_bot(bot=bot, categories=CATEGORIES)
