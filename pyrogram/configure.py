#!python

from pyrogram import Client
import configparser
import argparse

def config():
    print('config')

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
    return client

def init_app():
    config = init_config()
    parser = argparse.ArgumentParser(description='Get message from channels.')
    # config_group = parser.add_mutually_exclusive_group()
    parser.add_argument('--environment', '-e', choices=config.sections(), default='dev', action='store', help='Specify environment.')
    parser.add_argument('--list-config', '-lc', action='store_true', help='List all configuration.')
    args = parser.parse_args()
    if args.list_config:
        print(args)
        print(config.sections())
        exit()

    return init_client(config, args.environment)
