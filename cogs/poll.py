from discord.ext import commands
from config import prefix, bots, moderators, main_channel, poll_channel

voted = []


class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()  # tracks users voted and logs votes in file
    async def on_message(self, ctx):
        if str(ctx.channel) == poll_channel and str(ctx.author) not in bots:
            if prefix + 'post' not in str(ctx.content):
                await ctx.channel.purge(limit=1)

                if str(ctx.author) not in voted:
                    voted.append(str(ctx.author))
                    with open('poll_response.txt', 'a') as f:
                        f.write(str(ctx.content) + '\n')

    @commands.command()  # clears old poll data and posts a new poll
    async def post(self, ctx):
        if str(ctx.channel) == poll_channel and str(ctx.author) in moderators:

            voted.clear()
            with open('poll_response.txt', 'w'):
                pass

            await ctx.channel.purge(limit=1)
            await ctx.channel.send(ctx.message.content.replace(prefix + 'post', ''))

    @commands.command()  # calculates and displays the results of the current poll
    async def results(self, ctx):
        if str(ctx.channel) == main_channel and str(ctx.author) in moderators:
            response = ''
            results = {}

            with open('poll_response.txt', 'r') as f:
                for line in f:
                    for char in line:
                        if char.isdigit():
                            if char in results:
                                results[char] += 1
                            else:
                                results[char] = 1
                            break

                for key in sorted(results):
                    response += 'Option ' + key + ': ' + str(results[key]) + ' votes\n'
                await ctx.channel.send(response)


def setup(client):
    client.add_cog(Poll(client))
