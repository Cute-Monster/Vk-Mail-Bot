#!/bin/bash
echo "Rebooted" >> /home/pi/gmail_vk_bot/Logs/terminal.log
timedatectl | head -n 1 >> /home/pi/gmail_vk_bot/Logs/terminal.log
cd /home/pi/gmail_vk_bot/
source /home/pi/gmail_vk_bot/venv/bin/activate && /home/pi/gmail_vk_bot/venv/bin/python3.7 /home/pi/gmail_vk_bot/vkBot/main.py