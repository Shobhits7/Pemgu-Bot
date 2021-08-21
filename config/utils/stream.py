import discord
import youtube_dl

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "=vn"
}
YDL_OPTIONS = {
    "format": "bestaudio"
}

async def player(url):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" or url
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["formats"][0]["url"]
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        return source