import discord

class Confirm(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=3)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.clear_items()
        await interaction.response.edit_message(content="Confirmed", view=button.view)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.clear_items()
        await interaction.response.edit_message(content="Cancelled", view=button.view)
        self.stop()

    async def on_timeout(self):
        if self.children:
            self.clear_items()
            await self.message.edit(view=self)
    
    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.message.author.id:
            return True
        else:
            icheckmbed = discord.Embed(
                color=self.ctx.bot.color,
                title=F"You can't use this",
                description=F"<@{interaction.user.id}> - Only <@{self.ctx.message.author.id}> can use this\nCause they did the command\nIf you want to use this, do what they did",
                timestamp=interaction.message.created_at
            )
            icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
            return False
