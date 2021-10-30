import discord, difflib, traceback
from discord.ext import commands
from core.views import dymview

class OnError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CheckAnyFailure):
            return
        elif isinstance(error, commands.CommandNotFound):
            cmd = ctx.invoked_with
            cmds = [cmd.name for cmd in self.bot.commands]
            matches = difflib.get_close_matches(cmd, cmds)
            matcnfmbed = discord.Embed(
                color=self.bot.color,
                title=F"Couldn't find command called: {cmd}.",
                description=F"Maybe you meant:\n{' - '.join([match for match in matches])}",
                timestamp=ctx.message.created_at
            )
            matcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            nmatcnfmbed = discord.Embed(
                color=self.bot.color,
                title=F"Couldn't find command called: {cmd}.",
                description=F"Use help command to know what command you're looking for",
                timestamp=ctx.message.created_at
            )
            nmatcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            if len(matches) > 0:
                view = dymview.DYMView(ctx, matches)
                view.message = await ctx.send(embed=matcnfmbed)
            else:
                await ctx.send(embed=nmatcnfmbed)
        else:
            print("".join(traceback.format_exception(type(error), error,  error.__traceback__)))
            errormbed = discord.Embed(
                color=self.bot.color,
                title="❌ An Error Occurred",
                description=F"```diff\n- {error}\n```",
                timestamp=ctx.message.created_at
            )
            errormbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=errormbed)
    
def setup(bot):
    bot.add_cog(OnError(bot))