import discord, random
from discord.ext import commands

class JakeTheDogContext(commands.Context):
    async def send(self, content:str=None, embed:discord.Embed=None, **kwargs):
        if random.randint(1, 100) == 1:
            content = F"Since we need to have slash commands\nConsider inviting me again with `invite` command\n{content if content else ''}"
        if embed:
            embed.set_footer(text=F"Invoked by {self.author}", icon_url=self.author.default_avatar.url)
        return await super().send(content, embed, **kwargs)