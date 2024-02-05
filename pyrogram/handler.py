#!python

from pyrogram import filters
import configure

app, fltrs = configure.init_app()

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

@app.on_message(filters.chat("me") & filters.reply & filters.command('keep'))
async def message_hendler(client, message):
    print(message)
    await message.reply_to_message.react(emoji="✍") # NOTE fucking durov broke react in the saved messages need to rework concept
    await message.delete()

@app.on_message(filters.chat("me") & filters.reply & filters.command(commands='delete', prefixes=["/", "#"]))
async def message_hendler(client, message):
    print(message)
    await client.delete_messages(chat_id=message.chat.id, message_ids=[message.id, message.reply_to_message_id])

@app.on_message(filters.chat("me") & filters.reply & filters.command('nothing'))
async def message_hendler(client, message):
    await message.delete()

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
