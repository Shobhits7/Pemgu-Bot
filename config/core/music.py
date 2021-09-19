import discord, youtube_dl
from discord.ext import commands

class Music(commands.Cog, description="Jam out with these without needing to go to a party"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="connect", aliases=["join", "con"], help="Will join the bot to your voice")
    async def connect(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel")
        elif not ctx.voice_client:
            await ctx.send("Connected to your voice channel")
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Connected to your voice channel")
            await ctx.voice_client.move_to(ctx.author.voice.channel)

    @commands.command(name="disconnect", aliases=["dc"], help="Will disconnect the bot from voice channel")
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel")
        else:
            await ctx.send("I'm not in any voice channel")

    @commands.command(name="play", aliases=["pl"], help="Will play the given song")
    async def play(self, ctx, *, url):
        FFMPEG_OPTIONS = {"before_option": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        YDL_OPTIONS = {"format": "bestaudio"}
        if ctx.voice_client:
            ctx.voice_client.stop()
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.(url, download=False)
                print(info)
                url2 = info["format"][0]["url"]
                print(url2)
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                print(source)
                ctx.voice_client.play(source)

    @commands.command(name="pause", aliases=["pa"], help="Will pause the current song")
    async def pause(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.pause()
            await ctx.send("Paused the song")
        else:
            await ctx.send("I'm not in any voice channel")

    @commands.command(name="resume", aliases=["res"], help="Will resume the paused song")
    async def resume(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.resume()
            await ctx.send("Resuming the song")
        else:
            await ctx.send("I'm not in any voice channel")
        
def setup(bot):
    bot.add_cog(Music(bot))