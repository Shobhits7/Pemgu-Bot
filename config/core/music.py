import discord
from discord.ext import commands
from config.utils.stream import player

class Music(commands.Cog, description="Commands to jam out with"):
    def __init__(self, bot):
        self.bot = bot
    
    # Connect
    @commands.command(name="connect", aliases=["cn"], help="Will connect the bot to your voice channel")
    @commands.guild_only()
    async def connect(self, ctx):
        await ctx.trigger_typing()
        await ctx.author.voice.channel.connect()
    
    # Disconnect
    @commands.command(name="disconnect", aliases=["dc"], help="Will disconnect the bot to your voice channel")
    @commands.guild_only()
    async def disconnect(self, ctx):
        await ctx.trigger_typing()
        await ctx.voice_client.disconnect()
    
    # Play
    @commands.command(name="play", aliases=["p"], help="Will play the music given music in your voice channel", usage="<link>")
    async def play(self, ctx, *, url):
        await ctx.trigger_typing()
        await player(url)
    
    # Pause
    @commands.command(name="pause", aliases=["pa"], help="Will pause the song")
    @commands.guild_only()
    async def pause(self, ctx):
        await ctx.trigger_typing()
        await ctx.voice_client.pause()

    # Resume
    @commands.command(name="resume", aliases=["rs"], help="Will resume the song")
    @commands.guild_only()
    async def resume(self, ctx):
        await ctx.trigger_typing()
        await ctx.voice_client.resume()

    # Stop
    @commands.command(name="stop", aliases=["so"], help="Will stop the song")
    @commands.guild_only()
    async def stop(self, ctx):
        await ctx.trigger_typing()
        await ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Music(bot))