from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
from consts import *
if BITLY_ACTIVE == 1:
    import bitly_api

# This function allow us to create an HTML message to send
# You can edit all fields of message using HTML syntax

def create_item_html(items):
    response = []
    print(f'{5 * "*"} Creating post {5 * "*"}')
    
    if BITLY_ACTIVE == 1:
        connection = bitly_api.Connection(access_token=ACCESS_TOKEN)

    counter = 0

    # Shuffling items
    random.shuffle(items)

    # Iterate over items
    for item in items:
        # If item has an active offer
        if 'off' in item:

            # Creating buy button and Bitly Management
            if BITLY_ACTIVE == 1:
                shortlink = connection.shorten(uri = item['url'])
                keyboard = [
                    [InlineKeyboardButton("🛒 Questo libro è in offerta 🛒", callback_data='buy', url=shortlink['url'])],
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
