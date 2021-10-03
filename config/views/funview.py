import discord
from discord import colour

class NitroButton(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.ctx = view.ctx

    async def callback(self, interaction:discord.Interaction):
        anitrombed = discord.Embed(
            colour=self.ctx.bot.colour,
            title="Somebody claimed the Nitro.",
            description=F"{interaction.user} claimed the Nitro.",
            timestamp=interaction.message.created_at
        )
        anitrombed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
        self.label = "CLAIMED"
        self.style = discord.ButtonStyle.grey
        self.disabled = True
        await interaction.response.edit_message(embed=anitrombed, view=self.view)
        await interaction.response.send_message("https://imgur.com/NQinKJB", ephemeral=True)
class NitroView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=3)
        self.ctx = ctx
        self.add_item(item=NitroButton(label="ACCEPT", style=discord.ButtonStyle.green, view=self))

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if not item.disabled:
                    item.label = "EXPIRED"
                    item.style = discord.ButtonStyle.red
                    item.disabled = True
                    ontimeoutmbed = discord.Embed(
                        colour=self.ctx.bot.colour,
                        title="THE NITRO HAS EXPIRED",
                        description="The gift link has either expired or has been revoked.",
                        timestamp=self.ctx.message.created_at
                    )
                    ontimeoutmbed.set_footer(text=self.ctx.author, icon_url=self.ctx.author.display_avatar.url)
                    await self.message.edit(embed=ontimeoutmbed, view=self)