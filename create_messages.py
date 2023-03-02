from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
from consts import *
if BITLY_ACTIVE == 1:
    from bitlyshortener import Shortener

# This function allow us to create an HTML message to send
# You can edit all fields of message using HTML syntax
def create_item_html(items, forced:bool):
    response = []
    print(f'{5 * "*"} Creating post {5 * "*"}')

    counter = 0

    # Shuffling items
    random.shuffle(items)

    # Iterate over items
    if items is not None:
        for item in items:
            
            # If item has an active offer or a forced message
            if 'off' in item or forced == True:

                # Creating buy button and Bitly Management
                if BITLY_ACTIVE == 1:
                    tokens_pool = [ACCESS_TOKEN]
                    shortener = Shortener(tokens=tokens_pool, max_cache_size=8192)
                    shortlink_list = shortener.shorten_urls([item['url']])
                    shortlink = shortlink_list[0]
                    keyboard = [
                        [InlineKeyboardButton("🛒 Questo libro è in offerta 🛒", callback_data='buy', url=shortlink)],
                    ]
                else:
                    keyboard = [
                        [InlineKeyboardButton("🛒 Questo libro è in offerta 🛒", callback_data='buy', url=item['url'])],
                    ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Creating message body
                html = ""
                html += f"📚 <b>{item['title']}</b> \n"

                if 'description' in list(item.keys()):
                    html += f"{item['description']}\n"

                html += f"<a href='{item['image']}'>&#8205</a>\n"

                if 'savings' in list(item.keys()):
                    html += f"❌ Non più a: {item['original_price']}€ \n"

                html += f"💳 <b>In sconto a: {item['price']}</b> \n"

                if 'savings' in list(item.keys()):
                    html += f"🤑 <b>Risparmi: {item['savings']}€ (-{item['percentage']}%)</b> \n\n"

                html += f"<b><a href='{item['url']}'></a></b>"

                response.append(html)
                response.append(reply_markup)

                
                counter = counter + 1
                if counter == NUMBER_OF_MESSAGES:
                    break

        return response
