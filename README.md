# _**Bot which checks mailbox for new messages**_

Multiservice project which contains 3 parts:    
    - [IMAP service](###imapservice)
    - [Database service](###databaseservice)
    - [Vkontakte(Notification) service](###notificationservice)

## Service descriptions

### IMAP service

Service designed for login in specified mail server. After succesfull login `INBOX` folder is chosen and list of mewssages tagged with `UNSEEN` is requsted. List of emails is parsed to be verified by database module and send for user compiled by a specific pattern.


### Database service

Service which implements communications with `sqlite` database.
Constains ine table
```mysql
 CREATE TABLE SeenMessages(
    uid integer not null ,
    mess_text text not null
)
```
At which `mess_text` is stored as md5sum hash to optimize space utilization and searching/comparising speed.
This table is created automatically if isn't exists, so it is no need to do this manually.

### Notification service

Service which sends notifications via [VKontakte](https://vk.com).
This service triggers imap service to get new messages and checks them for existence at via database service.
After necessary checks filtered list is sent via notification for the specified user and chat, if chat is set up.


```TODO
Change IMAP service to lsten server for new messages in async mode
```

