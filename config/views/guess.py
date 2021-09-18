import discord, random
from discord.ext import commands

class HelpButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.client = view.client
        self.choose = view.choose
        self.number = view.number
    
    async def callback(self, interaction: discord.Interaction):
        if self.custom_id == self.number:
            self.choose = True
        else:
            self.choose = False
        if self.choose == True:
            truembed = discord.Embed(
                colour=self.client.color,
                title="You guessed correctly"
            )
            truembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=truembed)
        else:
            falsembed = discord.Embed(
                colour=self.client.color,
                title="You guessed incorrectly"
            )
            falsembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=falsembed)

class GuessView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=5)
        self.client = client
        self.choose = bool
        self.number = random.randint(1, 5)
        for _ in range(1, 6):
            self.add_item(item=HelpButtons(label=_, style=discord.ButtonStyle.blurple, custom_id=_, view=self))
    
    async def on_timeout(self):
        for item in self.children:
            self.clear_items()
            self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.blurple, disabled=True))
            self.add_item(discord.ui.Button(emoji="❌", label="Disabled due to timeout...", style=discord.ButtonStyle.red, disabled=True))
            await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.help.context.author.id:
            return True
        icheckmbed = discord.Embed(
            colour=self.help.context.bot.color,
            title="You can't use this",
            description=F"<@{interaction.user.id}> - Only <@{self.help.context.author.id}> can use that\nCause they did the command\nIf you wanted to use the command, do what they did",
            timestamp=self.help.context.message.created_at
        )
        icheckmbed.set_thumbnail(url=self.help.context.me.avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False