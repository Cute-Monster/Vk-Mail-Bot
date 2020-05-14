#!/bin/bash
cd /home/pi/gmail_vk_bot/
echo "Rebooted: " $( date ) >> src/Logs/terminal.log
source venv/bin/activate
python3.7 src/vkBot/main.py
