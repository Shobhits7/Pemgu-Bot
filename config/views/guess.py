import discord, random
from discord.ext import commands

class HelpButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.client = view.client
        self.choose = view.choose
        self.button = view.button
        self.number = view.number
        self.message = view.message
    
    async def callback(self, interaction: discord.Interaction):
        self.choose = True if self.custom_id == self.number else self.choose = False
        if self.choose == True:
            truembed = discord.Embed(
                colour=self.client.color,
                title="You guessed correctly"
            )
            truembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            self.message.edit(embed=truembed)
        else:
            falsembed = discord.Embed(
                colour=self.client.color,
                title="You guessed incorrectly"
            )
            falsembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            self.message.edit(embed=falsembed)

class GuessView(discord.ui.View):
    def __init__(self, client):
        self.client = client
        self.choose = None
        self.button = None
        self.number = random.randint(1, 5)
        for _ in range(1, 6):
            self.add_item(item=HelpButtons(label=_, style=discord.ButtonStyle.blurple, custom_id=_, view=self))
    
    async def on_timeout(self):
        try:
            ontimeoutmbed = discord.Embed(
                colour=self.client.color,
                title="You took so long to answer",
                description="Disabled due to timeout..."
            )
            self.clear_items()
            await self.message.edit(embed=ontimeoutmbed, view=self)
        except discord.NotFound:
            return

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