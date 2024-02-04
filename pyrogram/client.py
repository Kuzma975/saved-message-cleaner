#!python

from pyrogram import enums
from urllib.parse import urlparse
import configure
import random
import time

def count_domains(d, netloc):
    for item in netloc.split('.'):
        if d.get(item):
            d[item] += 1
        else:
            d[item] = 1
    return d

def count_entity(message, *ent):
    count = 0
    if message.entities:
        for entity in message.entities:
            if entity.type in ent:
                count += 1
    return count

def get_entities(message, *ent):
    e_list = list()
    for entity in message.entities:
        if entity.type in ent:
            e_list.append(message.text[entity.offset:entity.offset+entity.length])
    return e_list

action_text = "\n * '✍' - 'keep'\n * '🙈' - 'delete'\n * '🤷' - 'nothing'\n * '💊' - 'split'"
async def main():
    async with app:
        # "me" refers to your own chat (Saved Messages)
        async for message in app.get_chat_history("me", offset_id=26, limit=2):
            print(message)
            print(f'Hashtags in the message: {count_entity(message, enums.MessageEntityType.HASHTAG)}')
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
        # print(get_entities(message, enums.MessageEntityType.HASHTAG))

        ### Get chat with "me"
        # me_chat = await app.get_chat("me")
        # print(me_chat)
        # print(me_chat.pinned_message.text) # print latest pinned message

        print(f'Count messages with URL: {await app.search_messages_count("me", filter=enums.MessagesFilter.URL)}')
        count = 0
        domain_dict = dict()
        async for message in app.search_messages("me", filter=enums.MessagesFilter.URL):
            count += 1
            print(f'{count}:')
            url_entities_count = count_entity(message, enums.MessageEntityType.URL, enums.MessageEntityType.TEXT_LINK)
            print(f'URL entity count: {url_entities_count}')
            if url_entities_count > 1:
                print('Need to split (💊)')
            else:
                # print(message.entities)
                for entity in message.entities:
                    # print(entity)
                    if entity.type in [enums.MessageEntityType.URL, enums.MessageEntityType.TEXT_LINK]:
                        url = message.text[entity.offset:entity.offset+entity.length]
                        # print(f'Url is {url}')
                        parsed_url = urlparse(url)
                        domain_dict = count_domains(domain_dict, parsed_url.netloc)
                        # print(f'Parsed url: {parsed_url}')
                        if parsed_url.scheme == 'tg' or parsed_url.netloc ==  't.me':
                            print('This is Telegram url')
                        elif parsed_url.netloc == 'youtube.com' or parsed_url.netloc == 'www.youtube.com':
                            print('This is Youtube url')
            print(message.text)

            # print(message)
            time.sleep(2)
        print(domain_dict)
        ### find all pinned messages
        # async for message in app.search_messages("me", filter=enums.MessagesFilter.PINNED): # URL MENTION PHOTO
        #         print(message)

app, filters = configure.init_app()
print(f'Filters: {filters}')
app.run(main())
