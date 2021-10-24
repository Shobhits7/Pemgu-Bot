import discord, random
from discord.ext import commands

class PemguContext(commands.Context):
    async def send(self, content:str=None, embed:discord.Embed=None, **kwargs):
        if embed:
            if not embed.footer:
                embed.set_footer(text=F"Invoked by {self.author}", icon_url=self.author.display_avatar.url)
        if random.randint(0, 69) == 21:
            if "use_slash_commands" not in self.me.guild_permissions:
                content = F"{content}\n**Please re-invite me again for slash commands**\n> Since discord is forcing every bot to use slash commands `/` please re invite me again, with the command `.m invite`"
                return
            content = F"{content}\n**Go vote on top.gg**\n> https://top.gg/bot/844226171972616205"
            return
        return await super().send(content, embed, **kwargs)