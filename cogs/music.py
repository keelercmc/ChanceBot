import os
import discord
from discord.ext import commands
from discord.utils import get
from config import music_channel


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['j'])  # joins voice channel
    async def join(self, ctx):
        if str(ctx.channel) == music_channel and ctx.message.author.voice:
            global voice
            voice = get(self.client.voice_clients, guild=ctx.guild)
            channel = ctx.message.author.voice.channel

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

    @commands.command(aliases=['l'])  # leaves voice channel
    async def leave(self, ctx):
        if str(ctx.channel) == music_channel:
            await voice.disconnect()

    @commands.command(aliases=['p'])  # uses spotdl to parse a given link, search it on youtube, and download it
    async def play(self, ctx, url):

        if str(ctx.channel) == music_channel:

            music_path = r'C:\Users\Chance\Music\spotify_song.mp3'

            if os.path.exists(music_path):
                os.remove(music_path)

            cmd = 'spotdl --song ' + url
            os.system(cmd)

            ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio
                                                               (music_path)))

    @commands.command(aliases=['vol', 'v'])  # adjusts volume
    async def volume(self, ctx, vol: int):
        if str(ctx.channel) == music_channel:
            ctx.voice_client.source.volume = vol / 100


def setup(client):
    client.add_cog(Music(client))
