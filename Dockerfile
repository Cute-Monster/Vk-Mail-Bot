FROM python:3.8

RUN mkdir gmail_vk_bot

WORKDIR /home/pi/gmail_vk_bot

COPY ./Logs/ ./Logs
COPY ./Logger ./Logger
COPY ./ImapClient ./ImapClient
COPY ./VkNotifier ./VkNotifier
COPY ./SqlModule ./SqlModule
COPY ./db ./db
COPY ./startBot.py ./
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

RUN ls -la ./

ENTRYPOINT ["python", "startBot.py"]