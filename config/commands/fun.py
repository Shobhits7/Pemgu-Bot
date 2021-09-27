import discord
from discord.ext import commands

class Fun(commands.Cog, description="You sad?. Use these to at least have a smile"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nitro", help="Will gift free Nitro")
    async def nitro(self, ctx:commands.Context):
        class NitroButton(discord.ui.Button):
            def __init__(self, view, **kwargs):
                super().__init__(**kwargs)
            async def callback(self, interaction:discord.Interaction):
                if self.label == "Claim":
                    anitrombed = discord.Embed(
                        colour=self.bot.colour,
                        title="Somebody claimed the Nitro.",
                        description=F"{interaction.user} claimed the Nitro.",
                        timestamp=ctx.message.created_at
                    )
                    anitrombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
                    self.label = "Claimed"
                    self.style = discord.ButtonStyle.grey
                    self.disabled = True
                    await interaction.response.edit_message(embed=anitrombed, view=self.view)
                else:
                    print("ELSE")
        class NitroView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=15)
                self.add_item(item=NitroButton(label="Claim", style=discord.ButtonStyle.green, width=225, view=self))
            async def on_timeout(self):
                if self.children:
                    for item in self.children:
                        self.clear_items()
                        self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.red, disabled=True))
                        await self.message.edit(view=self)
        view = NitroView()
        bnitrombed = discord.Embed(
            colour=self.bot.colour,
            title="Click the button for claiming Nitro",
            timestamp=ctx.message.created_at
        )
        bnitrombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        view.message = await ctx.send(embed=bnitrombed, view=view)

def setup(bot):
    bot.add_cog(Fun(bot))
