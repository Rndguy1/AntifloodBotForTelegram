import telepot
from telepot.loop import MessageLoop
from threading import Thread, Timer
import time
from datetime import datetime, timedelta
from antiflood_config import token, antiflood_max_msgs, antiflood_seconds

user_ids = [] #list stores messages user_id
counter = {}  #dictionary of counters, organized by user id

def antiflood(user_id, chat_id):
    print('DEBUG - Values: user_id=' + str(user_id) + ' & chat_id=' + str(chat_id))
    if counter.get(user_id) is not None and counter.get(user_id) >= antiflood_max_msgs:
        date_time = datetime.now(None) + timedelta(seconds=60)
        bot.restrictChatMember(chat_id, user_id, until_date=date_time.timestamp(), can_send_messages=False)
        print("[!] " + str(user_id) + " was blocked because he has sent too many messages")
        
    counter[user_id] = 0

def on_message(msg):
    # main function to be used
    if msg['chat']['type'] == "supergroup" and "new_chat_member" not in msg and "left_chat_participant" not in msg:
        user_id = str(msg['from']['id'])
        if user_id not in user_ids:
            user_ids.append(user_id)
            counter[user_id] = 0
        if counter[user_id] == 0:
            Timer(antiflood_seconds, antiflood, [user_id, msg['chat']['id']]).start()
            counter[user_id] = counter[user_id] + 1
        else:
            counter[user_id] = counter[user_id] + 1

if __name__ == '__main__':
    # script starting point
    # defines telepot client
    bot = telepot.Bot(token)
    # loops the threaded main function
    MessageLoop(bot, on_message).run_as_thread()

    while True:
        # used for receiving updates repeatedly
        time.sleep(antiflood_seconds)
