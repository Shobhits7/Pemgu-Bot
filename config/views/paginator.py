import discord

class Paginator(discord.ui.View):
    def __init__(self, embeds:list):
        super().__init__(timeout=10)
        self.page = 0
        self.embeds = embeds

    @discord.ui.button(emoji="⏮", style=discord.ButtonStyle.green)
    async def previous(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.page += 1
        await interaction.response.edit_message(embed=self.embeds[self.page])

    @discord.ui.button(emoji="⏹", style=discord.ButtonStyle.red)
    async def stop(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.edit()

    @discord.ui.button(emoji="⏭", style=discord.ButtonStyle.green)
    async def next(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.page -= 1
        await interaction.response.edit_message(embed=self.embeds[self.page])
