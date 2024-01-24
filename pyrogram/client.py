#!python

from pyrogram import Client, enums
from pyrogram import filters
import configparser
import random

def init_config(config_file = '../config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    # config = database.get_configuration('pars2022')
    return config

def init_client(config, config_section = 'dev'):
    print('initiate client')
    client = Client(
        config[config_section]['session_file'],
        api_id=config[config_section]['api_id'],
        api_hash=config[config_section]['api_hash'],
        phone_number=config[config_section]['phone']
        )
    # client.start()
    # if not client.is_user_authorized():
    #     client.send_code_request(config[config_section]['phone'])
    #     try:
    #         client.sign_in(config[config_section]['phone'], input('Enter the code: '))
    #     except SessionPasswordNeededError:
    #         client.sign_in(password=input('Password: '))
    return client

def count_hashtags(message):
    count = 0
    if message.entities:
        for entity in message.entities:
            if entity.type is enums.MessageEntityType.HASHTAG:
                count += 1
    return count

action_text = "\n * '✍' - 'keep'\n * '🙈' - 'delete'\n * '🤷' - 'nothing'"
async def main():
    async with app:
        # "me" refers to your own chat (Saved Messages)
        async for message in app.get_chat_history("me", limit=1):
            print(message)
            print(f'Hashtags in the message: {count_hashtags(message)}')
        #     await app.send_message("me", f'What we shold do with this message?{action_text}', reply_to_message_id=message.id)
        #     await (await app.get_chat("me")).mark_unread()
            # await message.reply("What we shold do with this message?")
        message_count = await app.get_chat_history_count("me")
        message_ids = list()
        async for message in app.get_chat_history("me"):
            message_ids.append(message.id)
            if message.web_page:
                print(f'Site name is: {message.web_page.site_name}')
        
        # async for message in app.get_chat_history("me", offset_id=2, limit=1):
        #     print(message, end='\n')
        print(message_count)
        print(message_ids)

        ### get random message
        # random_message_id = random.choice(message_ids)
        # message = await app.get_messages("me", random_message_id)
        # print(message.text)

        ### reply for a random message
        # await app.send_message("me", "this is a reply", reply_to_message_id=random_message_id)
        # message = next(messages)

        ### Get HASHTAG from message
        # for entity in message.entities:
        #     if entity.type is enums.MessageEntityType.HASHTAG:
        #         print(message.text[entity.offset:entity.offset+entity.length])

        ### Get chat with "me"
        # me_chat = await app.get_chat("me")
        # print(me_chat)
        # print(me_chat.pinned_message.text) # print latest pinned message

        ### find all pinned messages
        # async for message in app.search_messages("me", filter=enums.MessagesFilter.PINNED):
        #         print(message)


config = init_config()
app = init_client(config)
emoji = {
    '👍': '',
    '✍': 'keep',
    '👎': '',
    '💩': '',
    '🔥': '',
    '🙈': 'delete',
    '🤷': 'nothing',
    '💊': 'split',
}
# app.run(main())
app.run(main())

@app.on_message()
async def message_hendler(client, message):
    print(message)

@app.on_edited_message(filters.chat("me"))
async def handle_reaction(client, message):
    print(f'message are income {message}')
    if message.reactions:
        action = emoji[message.reactions.reactions[0].emoji]
        if action == 'delete':
            print(message)
            await client.delete_messages(chat_id=message.chat.id, message_ids=[message.id, message.reply_to_message_id])
        elif action == 'keep':
            print(message)
            await message.reply_to_message.react(emoji="✍")
            await message.delete()
        elif action == 'nothing':
            await message.delete()
        else:
            print(f'{action} not implemented for reaction {emoji[message.reactions.reactions[0].emoji]}')
    # print(message.reactions.reactions[0].emoji)
### start handling messages
# app.run()
