FROM python:3.8

RUN mkdir -p /usr/app/gmail_vk_bot

WORKDIR /usr/app/gmail_vk_bot

ARG _MAIL_LINK=''
ARG _MAIL_USERNAME=''
ARG _MAIL_PASSWORD=''
ARG _DB_SEED=''
ARG _VK_API_TOKEN=''
ARG _VK_USERNAME=''
ARG _VK_PASSWORD=''
ARG _VK_ADMIN_ID=''

RUN echo "THIS IS MAIL_LINK $_MAIL_LINK"
# Setting up Env vars
ENV MAIL_LINK=$_MAIL_LINK
ENV MAIL_USERNAME=$_MAIL_USERNAME
ENV MAIL_PASSWORD=$_MAIL_PASSWORD
ENV DB_SEED=$_DB_SEED
ENV VK_API_TOKEN=$_VK_API_TOKEN
ENV VK_USERNAME=$_VK_USERNAME
ENV VK_PASSWORD=$_VK_PASSWORD
ENV VK_ADMIN_ID=$_VK_ADMIN_ID

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
