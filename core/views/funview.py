import discord, random

class CounterView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=5)
        self.ctx = ctx
        self.clicks = 0
        self.clickers = ""

    @discord.ui.button(emoji="👏", style=discord.ButtonStyle.green)
    async def click(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(view=button.view)
        self.clicks += 1
        if str(interaction.user) in self.clickers:
            pass
        else: self.clickers += F"{str(interaction.user)}\n"

    async def on_timeout(self):
        for item in self.children:
            self.clear_items()
        ontimeoutmbed = discord.Embed(
            colour=self.ctx.bot.colour,
            title=F"Button was clicked: {self.clicks} times",
        )
        if len(self.clickers) != 0 or self.clicks != 0:
            ontimeoutmbed.description = "People who clicked:\n"
            ontimeoutmbed.description += self.clickers
        else: ontimeoutmbed.description = "Nobody clicked the buttons"
        await self.message.edit(embed=ontimeoutmbed, view=self)

class NitroButton(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.ctx = view.ctx

    async def callback(self, interaction:discord.Interaction):
        await interaction.followup.send(content="https://i.imgur.com/NQinKJB.mp4", ephemeral=True)
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