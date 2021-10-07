import discord, io
from discord.ext import commands
from PIL import Image, ImageFilter

class Images(commands.Cog, description="Free Photoshop, without needing to know PSD"):
    def __init__(self, bot):
        self.bot = bot

    # Wanted
    @commands.command(name="wanted", help="Will make the user get wanted")
    async def wanted(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        wanted = Image.open("./core/images/wanted.jpg")
        data = io.BytesIO(await user.display_avatar.read())
        image = Image.open(data)
        image = image.resize((204, 204))
        wanted.paste(image, (108, 198))
        wanted.save("wanted.jpg")
        wantedmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} is now Wanted!",
            timestamp=ctx.message.created_at
        )
        wantedmbed.set_footer(text=user, icon_url=user.display_avatar.url)
        wantedmbed.set_image(url="attachment://wanted.jpg")
        await ctx.send(embed=wantedmbed, file=discord.File(fp="wanted.jpg"))

def setup(bot):
    bot.add_cog(Images(bot))