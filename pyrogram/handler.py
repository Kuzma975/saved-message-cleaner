#!python

"""Module to handle user reaction on messages"""

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
async def keep_command_hendler(client, message):
    """Function to handle `keep` command"""
    print(message)
    # NOTE fucking durov broke react in the saved messages
    # TODO need to rework concept
    await message.reply_to_message.react(emoji="✍")
    await message.delete()

@app.on_message(
    filters.chat("me")
    & filters.reply
    & filters.command(commands='delete', prefixes=["/", "#"]))
async def delete_command_hendler(client, message):
    """Function to handle `delete` command with different prefixes"""
    print(message)
    await client.delete_messages(
        chat_id=message.chat.id,
        message_ids=[message.id, message.reply_to_message_id])

@app.on_message(filters.chat("me")
                & filters.reply
                & filters.command('nothing'))
async def nothing_command_hendler(client, message):
    """Function to handle specific command `nothing`"""
    await message.delete()

@app.on_edited_message(filters.chat("me"))
async def handle_reaction(client, message):
    """Old function to handle react on messages"""
    print(f'message are income {message.id}')
    if not message.reply_to_message_id:
        print(f'Message {message.text} is not a reply message')
        return
    if message.reactions and message.reply_to_message_id:
        if len(message.reactions.reactions) > 0:
            income_emoji = message.reactions.reactions[0].emoji
            if income_emoji in emoji:
                action = emoji[income_emoji]
            else:
                print(f'Emoji not yet implemented {income_emoji}')
                return
            if action == 'delete':
                print(message)
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=[message.id,
                    message.reply_to_message_id])
            elif action == 'keep':
                print(message)
                await message.reply_to_message.react(emoji="✍")
                await message.delete()
            elif action == 'nothing':
                await message.delete()
            else:
                print(f'{action} not implemented for reaction {income_emoji}')
        else:
            print(f'There are not any reactions: {message}')
    # print(message.reactions.reactions[0].emoji)
### start handling messages
app.run()
