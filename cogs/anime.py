from discord.ext import commands
from config import anime_channel


class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Anime(client))
