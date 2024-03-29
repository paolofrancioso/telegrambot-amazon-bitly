# Amazon Offers Telegram Bot

This project is a Telegram Bot connected to a Telegram Channel that checks Amazon offers and send them to your Channel.
Original Project was from Samir Salman. This version adds a few options and has the Bitly functionalities embedded. Furthermore it increases performances limiting the number of calls to Amazon.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/paolofrancioso/telegrambot-amazon-bitly)

## Major Update: 20th February 2023

Now you can create a telegram group with this Bot as administrator and send him Amazon links. These will be translated in Offerings messages and they will be sent to the channel. For security reason it's necessary to set the SAFETY_CHAT_ID in consts.py. Please, add to your bot the followings commands (/setcommands):

- gen - Generate a post directly from an Amazon Link
- gid - Get your Chat ID

Create a Group with your telegram and use /gid to get the CHAT ID. Add it as SAFETY_CHAT_ID parameter. Now you can use /gen <url> where <url> is an amazon link to a product.

Run the new functionality as: ```python bot_actions.py``` or ```python3 bot_actions.py``` or ```nohup python3 bot_actions.py &```

or execute the new script to kill/startup both the processes: ```sh run.sh```



## Requirements

### SCRIPT INSTALLER

Now you can run the ```script.sh``` file from the terminal to install all dependencies, included paapi5 package. Open a terminal in the working directory, then type ```bash script.sh``` and launch the command. 



### MANUAL INSTALLER

In order to use this bot you must complete the following steps:

- Create a telegram bot (https://core.telegram.org/bots)
- Create an Amazon Affiliation (https://programma-affiliazione.amazon.it/)
- Create a Bitly Account and get a valid API_KEY (You activate this functionality in consts.py with parameter BITLY_ACTIVE = 1)
- Put all of your keys (Amazon and Telegram API Keys) in the code, we are going to define how below
- If you need to find host and region, please check latest documentation (currently here https://webservices.amazon.com/paapi5/documentation/common-request-parameters.html#host-and-region)
- Rename the file consts_template.py in consts.py and set all your Keys

- **Install packages**:
In the root of the project run:
```bash
pip3 install -r requirements.txt
cd paapi5-python-sdk
python3 setup.py build
python3 setup.py install
cd ..
```

## Project Structure

The project is organized like follow:

- **bot.py**
  - Contains the bot start code 

- **consts.py**
  - **HERE YOU MUST PUT YOUR TELEGRAM API KEYS AND PARAMETERS AND YOUR AMAZON API KEYS AND PARAMETERS**
  - **THE CHANNEL_NAME SHOULD START WITH @ (for example @MyChannelName)**
  

- **amazon_api.py**
  - Contain amazon api function to search products


- **response_parser.py**
  - Util functions that parse amazon api response


- **create_messages**
  - message creation functions

## How it works
The bot is running in a while loop, you can define your favorite parameters for:
- Hours of activity
- Pause time between messages
- Amazon Search Categories
- Search Keywords
- Minimum rating
- Minimum savings % (Amazon let it work only for some categories)



The bot is active if the time is between **MIN_HOUR** and **MAX_HOUR** (_you can deactivate it during the night for example_), you can define these parameters in the code.

The bot has a break for defined **PAUSE_MINUTE** after sending a message.

You can also edit message body in ```create_messages.py```.

The bot performs all http requests to Amazon API at start, saves a list of all results in RAM and as long as there are items in results list it:
1. SEND OFFER MESSAGE
2. PAUSE FOR PAUSE_MINUTES
3. SEND ANOTHER MESSAGE

during the activity time. When all results have been sent, it restarts his loop.

### **NOW YOU CAN SEARCH OVER MULTIPLE CATEGORIES** : _in `consts.py` you need to specify your categories and a list of keywords for each category. The corresponding variable is `categories`, it accept a dictionary like:_ 
```python
{
  "1_CATEGORY_NAME":[LIST OF KEYWORD],
  "2_CATEGORY_NAME":[LIST OF KEYWORD]
}
```
Important! Remember that currently Amazon supports only English Categories while you can use keywords in your language. Check Amazon API for info.

## Usage

After cloning the repository, define all parameters in the code, install all packages and then start bot with command:
```python bot.py``` or ```python3 bot.py``` or ```nohup python3 bot.py &```
  
## Support 
If you need support for the installation and usage of the library you can write to:
- freedogsconsulting@gmail.com
  
 
## Authors

- Paolo Francioso
