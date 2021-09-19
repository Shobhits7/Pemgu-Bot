import discord, youtube_dl, asyncio
from discord.ext import commands

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
FFMPEG_OPTIONS = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(YDL_OPTIONS)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

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
    async def play(self, ctx, link):
        if ctx.voice_client:
            ctx.voice_client.stop()
            player = await YTDLSource.from_url(url=link, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print("Player Error: %s" %e) if e else None)
            await ctx.send(F"Now playing: {player.title}")

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