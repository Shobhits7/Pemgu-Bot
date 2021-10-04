import discord, io
from discord.ext import commands
from PIL import Image, ImageFilter

class Image(commands.Cog, description="Free Photoshop, without needing to know anything"):
    def __init__(self, bot):
        self.bot = bot

    # Wanted
    @commands.command(name="wanted")
    async def wanted(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        pfp = user.avatar.url
        buffer = io.BytesIO(await pfp.read())
        wanted = Image.open("./images/wanted.jpg")
        final = Image.open(buffer)
        final = final.resize((300, 300))
        wanted.paste(final, (70, 2019))
        wanted.save(buffer, "jpg")
        buffer.seek(0)
        await ctx.send(file=discord.File(fp=buffer, filename="whatever.jpg"))

def setup(bot):
    bot.add_cog(Image)