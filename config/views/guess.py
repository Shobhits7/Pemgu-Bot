import discord, random
from discord.ext import commands

class HelpButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.bot = view.bot
        self.choose = view.choose
        self.number = view.number
    
    async def callback(self, interaction: discord.Interaction):
        if self.label == self.number:
            self.choose = True
        if self.label != self.number:
            self.choose = False
        else:
            await interaction.response.edit_message("self.choose has a problem")
        if self.choose == True:
            truembed = discord.Embed(
                colour=self.bot.color,
                title="You guessed correctly",
                description=F"The number was {self.number}"
            )
            truembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=truembed)
        if self.choose == False:
            falsembed = discord.Embed(
                colour=self.bot.color,
                title="You guessed incorrectly",
                description=F"The correct answer was {self.number}"
            )
            falsembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=falsembed)
        else:
            await interaction.response.edit_message("second self.choose has a problem")

class GuessView(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=5)
        self.bot = bot
        self.ctx = ctx
        self.choose = None
        self.number = random.randint(1, 5)
        for i in range(1, 6):
            self.add_item(item=HelpButtons(label=i, style=discord.ButtonStyle.green, view=self))
    
    async def on_timeout(self):
        for item in self.children:
            self.clear_items()
            self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.blurple, disabled=True))
            self.add_item(discord.ui.Button(emoji="❌", label="Disabled due to timeout...", style=discord.ButtonStyle.red, disabled=True))
            await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        icheckmbed = discord.Embed(
            colour=self.bot.color,
            title=F"You can't use this",
            description=F"<@{interaction.user.id}> - Only <@{self.ctx.author.id}> can use this\nCause they did the command\nIf you want to use this, do what they did",
            timestamp=interaction.message.created_at
        )
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False