# bot .py
import os
import discord
from escpos.printer import Usb


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# Printer Setup
p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
p.set(align='left')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:  # Do not respond to our bot messages
        return

    # Timestamp
    p.text(message.created_at.strftime('%Y/%m/%d-%H:%M:%S'))
    p.ln()
    print(message.created_at)
    # Author
    p.set(invert=True)
    p.text(message.author.name)
    p.set(invert=False)
    p.ln()
    print(message.author.name)
    # Message
    p.text(message.content)
    p.ln()
    print(message.content)
    p.ln(7)


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as errorFile:
        if event == 'on_message':
            errorFile.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
