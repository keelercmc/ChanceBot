from discord.ext import commands


class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ponged in')


def setup(client):
    client.add_cog(Anime(client))
