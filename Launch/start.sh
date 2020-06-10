#!/bin/bash -i
# cd /home/pi/gmail_vk_bot/
echo "Rebooted: " $( date ) >> /home/pi/gmail_vk_bot/Logs/terminal.log
# source venv/bin/activate
/home/pi/gmail_vk_bot/venv/bin/python3.7 main.py
