import discord, random
from discord.ext import commands

class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command(self, ctx:commands.Context):
        if random.randint(0, 10) == 9:
            rimbed = discord.Embed(
                color=self.bot.color,
                title="Please re-invite me again for slash commands",
                description="Since discord is forcing every bot to use slash commands `/` please re invite me again, with the command `.m invite`",
                timestamp=ctx.message.created_at
            )
            rimbed.set_footer(text="From the Pemgu-Bot Developers", icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=rimbed)

def setup(bot):
    bot.add_cog(OnCommand(bot))