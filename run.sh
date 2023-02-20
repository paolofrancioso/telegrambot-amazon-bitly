pkill -f bot.py
pkill -f bot_actions.py
bash -c "exec nohup python3 bot.py &> nohup_bot.out &"
bash -c "exec nohup python3 bot_actions.py &> nohup_actions.out &"