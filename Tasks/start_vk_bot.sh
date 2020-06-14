#!/bin/bash -i
# cd /home/pi/gmail_vk_bot/
echo "Started: " $( date ) >> /home/pi/gmail_vk_bot/Logs/terminal.log
# source venv/bin/activate
cd /home/pi/gmail_vk_bot/
/home/pi/gmail_vk_bot/venv/bin/python3.7 startBot.py
