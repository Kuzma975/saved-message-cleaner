#!python

from pyrogram import Client, enums
import configparser

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


async def main():
    async with app:
        # "me" refers to your own chat (Saved Messages)
        async for message in app.get_chat_history("me", limit=1):
            for entity in message.entities:
                if entity.type is enums.MessageEntityType.HASHTAG:
                    print(message.text[entity.offset:entity.offset+entity.length])

config = init_config()
app = init_client(config)
app.run(main())
