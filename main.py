import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')
client.remove_command('help')
prefix = '.'
moderators = ['Chance#0017']

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print('Logged in')


@client.event
async def on_message(message):
    with open('messages.txt', 'a') as f:
        f.write(str(message.author) + '\n')
    await client.process_commands(message)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Commands")
    embed.add_field(name="Help", value="Shows this block.")
    embed.add_field(name="Messages", value="Shows the number of messages the user has sent.")
    embed.add_field(name="Anime", value="N/A.")
    embed.add_field(name="Play", value="N/A.")
    await ctx.channel.send(content=None, embed=embed)


@client.command()
async def messages(ctx):
    with open('messages.txt', 'r') as f:
        messageList = f.readlines()
        messageList = [m.strip() for m in messageList]
        await ctx.channel.send(str(ctx.message.author.name) + ' has sent ' +
                               str(messageList.count(str(ctx.message.author))) + ' messages.')


@client.command()
async def clear(ctx):
    if str(ctx.message.author) in moderators:
        limit = 10
        if str(ctx.message.content) > prefix + 'clear':
            limit = int(ctx.message.content.replace(prefix + 'clear ', ''))
        await ctx.channel.purge(limit=limit)


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client.run(token)
