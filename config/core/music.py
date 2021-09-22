import discord
import aqualink
from discord.ext import commands
from datetime import timedelta


class Music:
    def __init__(self, bot):
        self.playlist_urls = (
            "https://youtube.com/playlist",
            "https://youtu.be/",
            "https://www.youtube.com/playlist",
        )
        self.bot = bot
        self.queue = {}
        bot.loop.create_task(self.connect())

    async def connect(self):
        aqualink.Connection.connect_to(self.bot)
        await self.bot.aqualink.connect(
            password="youshallnotpass",
            ws_url="ws://localhost:2333",
            rest_url="http://localhost:2333",
        )

    async def track_callback(self, player):
        queue_data = self.queue[player.guild]
        if not queue_data[1]:
            await player.disconnect()
            del self.queue[player.guild]
        else:
            track = queue_data[1].pop(0)
            await player.play(track)
            await queue_data[0].send(f"Playing {track.title}")

    # Play
    @commands.command(name="play", help="Will play or add the given song ot the queue", usage="<query>")
    async def play(self, ctx, *, query: str):
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not ctx.guild.me.voice:
            await player.connect(ctx.author.voice.channel.id)
        if query.startswith(self.playlist_urls):
            is_playlist = True
            tracks = await player.query(query)
        else:
            is_playlist = False
            tracks = await player.query(f"ytsearch: {query}")
        track = tracks[0]
        if self.queue.get(ctx.guild):
            if is_playlist:
                self.queue[ctx.guild][1].extend(tracks)
                await ctx.send(
                    f"Added a playlist with {len(tracks)} tracks to the queue."
                )
            else:
                self.queue[ctx.guild][1].append(track)
                await ctx.send(f"Added {track.title} to the queue")
        else:
            if is_playlist:
                self.queue[ctx.guild] = [ctx.channel, tracks[1:]]
                await player.play(track)
                await ctx.send(f"Playing a playlist with {len(tracks)} tracks.")
            else:
                self.queue[ctx.guild] = [ctx.channel, []]
                await player.play(track)
                await ctx.send(f"Playing {track.title}")
        player.track_callback = self.track_callback

    # Skip
    @commands.command(name="skip", aliases=["pass"], help="Will skip the current song")
    async def skip(self, ctx):
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if player.paused or player.playing:
            await player.stop()
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("I'm not playing...")

    # Queue
    @commands.command(name="queue", aliases=["q"], help="Will Show up to 5 queued songs")
    async def _queue(self, ctx):
        player = self.bot.aqualink.get_player(ctx.guild.id)
        queue = self.queue.get(ctx.guild)
        if not queue:
            return await ctx.send("I am not playing at all.")
        queue = queue[1][:5]
        if not queue:
            return await ctx.send("No more upcoming tracks...")
        queue_text = "\n".join(f"{t.title} by {t.author}" for t in queue)
        await ctx.send(queue_text)

    # NowPlaying
    @commands.command(name="nowplaying", aliases=["np"], help="Will show the current song that is being played")
    async def now_playing(self, ctx):
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not player.track:
            return await ctx.send("I'm not playing anything.")
        track = player.track
        em = discord.Embed(title=f"Playing in {ctx.guild}")
        em.add_field(name="Track", value=track.title)
        em.add_field(name="Author", value=track.author)
        em.add_field(name="Length", value=str(timedelta(milliseconds=track.length)))
        em.add_field(name="Position", value=str(timedelta(milliseconds=track.position)))
        em.add_field(name="Volume", value=f"{player.volume}%")
        em.set_thumbnail(url=track.thumbnail)
        await ctx.send(embed=em)

    # Volume
    @commands.command(name="volume", aliases=["vol"], help="Will set the volume to the given amount", usage="<vol>")
    async def volume(self, ctx, vol: int):
        if vol < 0 or vol > 150:
            return await ctx.send(
                "Must be smaller than 151 and bigger than or equal to 0."
            )
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not player.playing:
            return await ctx.send("I'm not playing!")
        await player.set_volume(vol)
        await ctx.send(f"Volume set to {vol}%")

    # Stop
    @commands.command(name="stop", help="Will stop the current song, and will leave the voice")
    async def stop(self, ctx):
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not player.connected or not ctx.guild.me.voice:
            return await ctx.send("I'm not playing.")
        player.track_callback = None
        del self.queue[ctx.guild]
        await player.stop()
        await player.disconnect()
        await ctx.send("Stopped.")


def setup(bot):
    bot.add_cog(Music(bot))