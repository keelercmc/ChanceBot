from discord.ext import commands


class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Anime(client))
