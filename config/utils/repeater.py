import discord

class Repeater(discord.ui.View):
    def __init__(self, bot, job:function):
        super().__init__(timeout=5)
        self.bot = bot
        self.job = job

    @discord.ui.button(emoji="🔁")
    async def repeat(self, button:discord.ui.Button, interaction:discord.Interaction):
        await self.job

