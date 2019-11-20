import os
import discord
from discord.ext import commands
from config import prefix, moderators, main_channel, music_channel, osrs_channel, poll_channel
import pyowm

client = commands.Bot(command_prefix=prefix, case_insensitive=True)
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
        embed = discord.Embed(title='Commands')
        embed.add_field(name='Help', value='#' + main_channel + '\n\nShows this block.')
        embed.add_field(name='Messages', value='#' + main_channel + '\n\nShows the number of messages the user has sent.')
        embed.add_field(name='Leaderboard', value='#' + main_channel + '\n\nShows a ranking of the users with the most messages.')
        embed.add_field(name='Weather', value='#' + main_channel + '\n\nShows the temperature of a city.')
        embed.add_field(name='Stats', value='#' + osrs_channel + '\n\nShows a user\'s OSRS stats.')
        embed.add_field(name='Prices', value='#' + osrs_channel + '\n\nShows an item\'s trade value.')
        embed.add_field(name='Join', value='#' + music_channel + '\n\nRequests bot to join your voice chat.')
        embed.add_field(name='Leave', value='#' + music_channel + '\n\nRequests bot to leave your voice chat.')
        embed.add_field(name='Play', value='#' + music_channel + '\n\nPlays a Spotify URL')
        embed.add_field(name='Volume', value='#' + music_channel + '\n\nAdjusts volume (0-100)')
        await ctx.channel.send(content=None, embed=embed)


@client.command()  # displays mod help dialogue
async def modhelp(ctx):
    if str(ctx.channel) == main_channel and str(ctx.author) in moderators:
        embed = discord.Embed(title='Commands')
        embed.add_field(name='ModHelp', value='#' + main_channel + '\n\nShows this block.')
        embed.add_field(name='Clear', value='#' + main_channel + '\n\nClears messages.')
        embed.add_field(name='Post', value='#' + poll_channel + '\n\nPosts a new poll question.')
        embed.add_field(name='Results', value='#' + poll_channel + '\n\nShows the results of a poll.')
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


@client.command()  # displays the users with the most messages sent
async def leaderboard(ctx):
    rank = 0
    scores = {}
    response = ''
    results = 10

    if str(ctx.message.content) > prefix + 'leaderboard':
        if int(ctx.message.content.replace(prefix + 'leaderboard ', '')) <= 50:
            results = int(ctx.message.content.replace(prefix + 'leaderboard ', ''))

    with open('messages.txt', 'r') as f:
        messages_file = f.readlines()
        messages_file = [m.strip() for m in messages_file]

        for guild in client.guilds:
            for member in guild.members:
                member = str(member)
                scores[member] = str(messages_file.count(member))

        for score in sorted(scores, key=scores.get, reverse=True):

            if rank < results:
                rank += 1
                response += '#' + str(rank) + ' - ' + scores[score] + ' - ' + score + '\n'

    await ctx.channel.send('```Leaderboard\n\n' + response + '```')


@client.command(aliases=['w'])  # shows the weather stats in a given city using OpenWeatherMap API
async def weather(ctx, city):
    if str(ctx.channel) == main_channel:
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        f = w.get_temperature('fahrenheit')
        c = w.get_temperature('celsius')
        await ctx.channel.send('The temperature in ' + city.title() + ' is ' +
                               str(round(f['temp'])) + 'F / ' + str(round(c['temp'])) + 'C.\n' +
                               'High: ' + str(round(f['temp_max'])) + 'F / ' + str(round(c['temp_max'])) +
                               'C, Low: ' + str(round(f['temp_min'])) + 'F / ' + str(round(c['temp_min'])) + 'C.')


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


def read_owm():  # reads OpenWeatherMap API key
    with open('owm_key.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


owm = pyowm.OWM(read_owm())
token = read_token()
client.run(token)
