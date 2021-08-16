import discord
from discord.ext import commands
import datetime

class Fun(commands.Cog, name="Fun :rofl:", description="Very Funny commands"):
    def __init__(self, bot):
        self.bot = bot
    
    # Treesome
    @commands.command(name="treesome", aliases=["ts"], help="Gives a ticket to an Treesome Party")
    async def treesome(self, ctx):
        await ctx.trigger_typing()
        tsmbed = discord.Embed(
            colour=self.bot.color,
            title="So you are really this horny 😐😑\nBut anyway here get some trees 🌳🌲🎄🎋🌴",
            timestamp=ctx.message.created_at
        )
        tsmbed.set_image(url="https://cdn.discordapp.com/attachments/873478114183880704/875570208629198890/matt-artz-nTRDnDdDYk8-unsplash.png")
        tsmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=tsmbed)

    # Echo
    @commands.command(name="echo", aliases=["eo"], help="Will echo your message", usage="<text>")
    async def echo(self, ctx, *, echo):
        await ctx.trigger_typing()
        badeombed = discord.Embed(
            colour=self.bot.color,
            title="Don't even think of using that",
            timestamp=ctx.message.created_at
        )
        badeombed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if "@everyone" in ctx.message.content or "@here" in ctx.message.content:
            if ctx.author.guild_permissions.mention_everyone:
                return await ctx.reply(echo)
            return await ctx.reply(embed=badeombed)
        else:
            await ctx.reply(echo)

def setup(bot):
    bot.add_cog(Fun(bot))
