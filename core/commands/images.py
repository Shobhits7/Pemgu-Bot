import discord
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageFilter

class Images(commands.Cog, description="Free Photoshop, without needing to know PSD"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="wanted", help="Will make the user get wanted")
    async def wanted(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        wanted = Image.open("./core/images/wanted.jpg")
        asset = user.display_avatar
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((204, 204))
        wanted.paste(pfp, (108, 200))
        wanted.save("wanted.gif")
        wantedmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} is now Wanted!",
            timestamp=ctx.message.created_at
        )
        wantedmbed.set_footer(text=user, icon_url=user.display_avatar.url)
        wantedmbed.set_image(url="attachment://wanted.gif")
        await ctx.send(embed=wantedmbed, file=discord.File(fp="wanted.gif"))

def setup(bot):
    bot.add_cog(Images(bot))