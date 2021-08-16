import discord
from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self, ctx):
        print(F"---------------------------------------------------\nLogged in as: {self.bot.user} - {self.bot.user.id}\nMain prefix is: ~b\nThe Bot  is online now\n---------------------------------------------------")

        msgchannel = self.bot.get_channel(873472317114679336)
        onlinembed= discord.Embed(
            colour=self.bot.color,
            title="Bot is online now",
            timestamp=ctx.message.created_at
        )
        onlinembed.set_footer(text="You can use the commands now", icon_url=ctx.me.avatar_url)
        await msgchannel.send(embed=onlinembed)


def setup(bot):
    bot.add_cog(OnReady(bot))
