from discord.ext import commands

prefix = '.'
channels = ['polls']
moderators = ['Chance#0017']


class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Poll(client))
