from discord.ext import commands
from config import prefix, osrs_channel
from OSRSBytes import Hiscores, Items


class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()  # makes API request to look up a given user's stats
    async def stats(self, ctx):
        if str(ctx.channel) == osrs_channel:
            query = ctx.message.content.split(' ')

            if query[3] == 'x' or query[3] == 'xp':
                query[3] = 'experience'
            elif query[3] == 'l' or query[3] == 'lvl':
                query[3] = 'level'
            elif query[3] == 'r':
                query[3] = 'rank'

            player = Hiscores(query[1], 'N')
            response = player.skill(query[2], query[3])
            await ctx.channel.send(query[1].title() + '\'s ' + query[2].title() + ' ' +
                                   query[3] + ' is ' + str(f'{int(response):,d}') + '.')

    @commands.command()  # makes API request to look up a given item's market value
    async def prices(self, ctx):
        item = str(ctx.message.content.replace(prefix + 'prices ', ''))
        buy = Items().getBuyAverage(item)
        sell = Items().getSellAverage(item)
        alch = Items().getHighAlchValue(item)
        response = '```' + item.title() + '\n' + '\nAverage buying price: ' + str(buy) + '\nAverage selling price: ' + str(sell) + '\nHigh alchemy value: ' + str(alch) + '```'
        await ctx.channel.send(response)


def setup(client):
    client.add_cog(Anime(client))
