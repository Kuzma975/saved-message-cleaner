#!python

from pyrogram import filters
import configure

app = configure.init_app()

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

@app.on_message()
async def message_hendler(client, message):
    print(message)

@app.on_edited_message(filters.chat("me"))
async def handle_reaction(client, message):
    print(f'message are income {message.id}')
    if not message.reply_to_message_id:
        print(f'Message {message.text} is not a reply message')
        return
    if message.reactions and message.reply_to_message_id:
        if len(message.reactions.reactions) > 0:
            if message.reactions.reactions[0].emoji in emoji.keys:
                action = emoji[message.reactions.reactions[0].emoji]
            else:
                print(f'Emoji not yet implemented {message.reactions.reactions[0].emoji}')
                return
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
        else:
            print(f'There are not any reactions: {message}')
    # print(message.reactions.reactions[0].emoji)
### start handling messages
app.run()
