_**Bot which checks mailbox for new messages**_
    
    1) Check for messages in INBOX folder at defined mailbox
    2) Parse found messages info to:
        a) From
        b) Subject
        c) Text
        d) Has attachments
    3) If all message info represented as hash isn't in DataBase:
        Notify by Vk about new message by sending parsed message info