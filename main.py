import discord
from discord.ext import commands
import os
from config import prefix, moderators, main_channel

client = commands.Bot(command_prefix='.')
client.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event  # logs when bot connects
async def on_ready():
    print('Logged in')


@client.event  # logs messages to a txt file
async def on_message(message):
    with open('messages.txt', 'a') as f:
        f.write(str(message.author) + '\n')
    await client.process_commands(message)


@client.command()  # displays help dialogue
async def help(ctx):
    if str(ctx.channel) == main_channel:
        embed = discord.Embed(title="Commands")
        embed.add_field(name="Help", value="#general\n\nShows this block.")
        embed.add_field(name="Messages", value="#general\n\nShows the number of messages the user has sent.")
        embed.add_field(name="Anime", value="#anime\n\nN/A.")
        embed.add_field(name="Play", value="#music\n\nN/A.")
        await ctx.channel.send(content=None, embed=embed)


@client.command()  # displays number of messages a given user has sent
async def messages(ctx):
    if str(ctx.channel) == main_channel:
        with open('messages.txt', 'r') as f:
            messages_file = f.readlines()
            messages_file = [m.lower().strip() for m in messages_file]

            if str(ctx.message.content) > prefix + 'messages':
                user = ctx.message.content.replace(prefix + 'messages ', '')
            else:
                user = ctx.message.author

            await ctx.channel.send(str(user) + ' has sent ' +
                                   str(messages_file.count(str(user).lower())) + ' messages.')


@client.command()  # clears messages
async def clear(ctx):
    if str(ctx.message.author) in moderators:
        limit = 10
        if str(ctx.message.content) > prefix + 'clear':
            limit = int(ctx.message.content.replace(prefix + 'clear ', ''))
        await ctx.channel.purge(limit=limit)


def read_token():  # reads token in
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client.run(token)
