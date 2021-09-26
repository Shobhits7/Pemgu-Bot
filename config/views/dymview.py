import discord

class DYMButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.bot = view.bot
        self.ctx = view.ctx
        self.matches = view.matches

    async def callback(self, interaction:discord.Interaction):
        for match in self.matches:
            if self.label == match:
                await interaction.message.delete()
                await self.bot.process_commands(self.ctx.message)
        if self.label == "Delete":
            deletembed = discord.Embed(
                colour=self.bot.colour,
                title="Deleted the message",
                timestamp=interaction.message.created_at
            )
            deletembed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.message.delete()
            await interaction.response.send_message(embed=deletembed, ephemeral=True)

class DYMView(discord.ui.View):
    def __init__(self, bot, ctx, matches):
        super().__init__(timeout=10)
        self.bot = bot
        self.ctx = ctx
        self.matches = matches
        for match in self.matches:
            self.add_item(item=DYMButtons(label=match, style=discord.ButtonStyle.green, view=self))
        self.add_item(item=DYMButtons(emoji="💣",label="Delete", style=discord.ButtonStyle.red, custom_id="Delete", view=self))
    
    async def on_timeout(self):
        try:
            if self.children:
                for item in self.children:
                    self.clear_items()
                    self.add_item(discord.ui.Button(emoji="❌", label="You took so long to answer...", style=discord.ButtonStyle.blurple, disabled=True))
                    self.add_item(discord.ui.Button(emoji="💣", label="Disabled due to timeout...", style=discord.ButtonStyle.red, disabled=True))
                    await self.message.edit(view=self)
        except discord.NotFound:
            pass

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            icheckmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"You can't use this",
                description=F"<@{interaction.user.id}> - Only <@{self.ctx.author.id}> can use this\nCause they did the command\nIf you want to use this, do what they did",
                timestamp=interaction.message.created_at
            )
            icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
            return False