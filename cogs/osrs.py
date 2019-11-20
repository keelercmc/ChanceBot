from discord.ext import commands
from config import prefix, osrs_channel
from OSRSBytes import Hiscores, Items


class Osrs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['hiscores'])  # makes API request to look up a given user's stats
    async def stats(self, ctx, player, skill, attribute):
        if str(ctx.channel) == osrs_channel:

            if attribute == 'x' or attribute == 'xp':
                attribute = 'experience'
            elif attribute == 'l' or attribute == 'lvl':
                attribute = 'level'
            elif attribute == 'r':
                attribute = 'rank'

            stats = Hiscores(player, 'N')
            response = stats.skill(skill, attribute)
            await ctx.channel.send(player.title() + '\'s ' + skill.title() + ' ' +
                                   attribute + ' is ' + str(f'{int(response):,d}') + '.')

    @commands.command()  # makes API request to look up a given item's market value
    async def prices(self, ctx):
        item = str(ctx.message.content.replace(prefix + 'prices ', ''))
        buy = Items().getBuyAverage(item)
        sell = Items().getSellAverage(item)
        alch = Items().getHighAlchValue(item)
        response = '```' + item.title() + '\n' + '\nAverage buying price: ' + str(buy) + '\nAverage selling price: ' + str(sell) + '\nHigh alchemy value: ' + str(alch) + '```'
        await ctx.channel.send(response)


def setup(client):
    client.add_cog(Osrs(client))
