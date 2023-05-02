from telethon import TelegramClient, sync
from telethon.errors import SessionPasswordNeededError
import db
import configparser
import argparse

# TODO (add ) apply changes to db (chat id column)
# TODO (add table with chat list) add info about channels

def init_config(config_file = 'config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    # config = database.get_configuration('pars2022')
    return config

def init_client(config, config_section = 'dev'):
    print('initiate client')
    client = TelegramClient(
        config[config_section]['session_file'],
        config[config_section]['api_id'],
        config[config_section]['api_hash']
        )
    client.start()
    if not client.is_user_authorized():
        client.send_code_request(config[config_section]['phone'])
        try:
            client.sign_in(config[config_section]['phone'], input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    return client

def init_database(config, config_section = 'dev'):
    database = db.Baza(
        db_file=config[config_section]['database_file'],
        create_tables=config.getboolean(config_section, 'create_tables')
        )
    return database

def configure_channels(client, database):
    for dialog in client.iter_dialogs():
        if dialog.is_channel and 'повістки' in dialog.title:
            answer = input(f'Do you want to monitor the "{dialog.title}" channel? (yes or no) ')
            if answer.lower() in ['yes', 'y', '1', 't', 'true']:
                city = input('What is the city? ')
                print(f'database.insert_channel({dialog.id}, {city}, {dialog.title})')
                database.insert_channel(dialog.id, city, dialog.title)
            else:
                print(f'The "{dialog.title}" will be skipped')

def read_messages(client, database):
    for i in database.get_channels():
        for message in client.get_messages(i['channel_id'], limit=10):

            print(f'chat id is {message.chat_id}')

            chat = message.get_chat()
            print(chat.id)
            print(chat.title)
            print(message.text)
            print(message.id)
            print(message.date)
            if message.id == 1:
                message.mark_read()
            database.insert_message(message.id, message.chat_id, message.text, message.date.timestamp())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get message from channels.')
    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument('--config', '-c', action='store_true', help='Configure channels.')
    config_group.add_argument('--list-config', '-lc', action='store_true', help='List all configuration.')
    args = parser.parse_args()
    print(args)
    config = init_config()
    client = init_client(config)
    database = init_database(config)
    if args.config:
        configure_channels(client, database)
    elif args.list_config:
        print("list all config")
    else:
        print("else")
    read_messages(client, database)
    database.close()