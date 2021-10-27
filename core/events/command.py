import discord, random
from discord.ext import commands

class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command(self, ctx:commands.Context):
        number = random.randint(0, 100)
        if number == 55:
            if "use_slash_commands" not in ctx.me.guild_permissions:
                scmdmbed = discord.Embed(
                    color=self.bot.color,
                    title="Please re-invite me again for slash commands",
                    description="Since discord is forcing every bot to use slash commands `/` please re invite me again, with the command `.m invite`",
                    timestamp=ctx.message.created_at
                )
                await ctx.send(embed=scmdmbed)
        if number == 70:
            votembed = discord.Embed(
                color=self.bot.color,
                url="https://top.gg/bot/844226171972616205",
                title="Go vote on top.gg",
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=votembed)

def setup(bot):
    bot.add_cog(OnCommand(bot))