from discord.ext import commands

prefix = '.'
channels = ['polls']
moderators = ['Chance#0017']


class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx):
        if str(ctx.message.channel) in channels and str(ctx.message.author) in moderators:
            if str(ctx.message.content) > prefix + 'clear':
                limit = int(ctx.message.content.replace(prefix + 'clear ', ''))
            else:
                limit = 125
            await ctx.channel.purge(limit=limit)


def setup(client):
    client.add_cog(Poll(client))
