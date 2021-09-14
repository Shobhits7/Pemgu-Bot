import discord
from discord.ext import commands

class CounterView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=5)
        self.clicks = 0
        self.client = client

    async def on_timeout(self):
        ontimeoutmbed = discord.Embed(
            colour=self.client.color,
            title=F"Button was clicked {self.clicks} times"
        )
        await self.message.edit(embed=ontimeoutmbed, view=self)

    @discord.ui.button(label="➕1", style=discord.ButtonStyle.blurple)
    async def Plus1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clicks + 1
    
    @discord.ui.button(label="➖1", style=discord.ButtonStyle.red)
    async def Minus1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clicks - 1