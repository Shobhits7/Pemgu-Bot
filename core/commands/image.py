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
        wanted = Image.open("./images/wanted.jpg")
        pfp = user.avatar.url
        buffer = io.BytesIO(await pfp.read())
        image = Image.open(buffer)
        image = image.resize((300, 300))
        wanted.paste(image, (70, 2019))
        wanted.save(buffer, "jpg")
        buffer.seek(0)
        final = io.BytesIO(await image.read())
        await ctx.send(file=discord.File(fp=final, filename="whatever.jpg"))

def setup(bot):
    bot.add_cog(Image(bot))