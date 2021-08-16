import discord
from discord.ext import commands
import datetime
import difflib
import traceback
import sys

class OnError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.trigger_typing()
        if isinstance(error, commands.NotOwner):
            nombed = discord.Embed(
                colour=self.bot.color,
                title="You are not the owner of this bot",
                timestamp=ctx.message.created_at
            )
            nombed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nombed)
        elif isinstance(error, commands.CommandNotFound):
            cmd = ctx.invoked_with
            cmds = [cmd.name for cmd in self.bot.commands]
            matches = difflib.get_close_matches(cmd, cmds)
            matcnfmbed = discord.Embed(
                colour=self.bot.color,
                title=F"There is no `{cmd}` command",
                description=F"Maybe you meant `{matches}`",
                timestamp=ctx.message.created_at
            )
            matcnfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            nmatcnfmbed = discord.Embed(
                colour=self.bot.color,
                title=F"There is no `{cmd}` command",
                description="Use `~b help` command to know what command are there",
                timestamp=ctx.message.created_at
            )
            nmatcnfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            if len(matches) > 0:
                await ctx.reply(embed=matcnfmbed)
            else:
                await ctx.reply(embed=nmatcnfmbed)
        elif isinstance(error, commands.MissingPermissions):
            mpmbed = discord.Embed(
                colour=self.bot.color,
                title=F"You don't have permission for {ctx.command}",
                timestamp=ctx.message.created_at
            )
            mpmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=mpmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            bmpmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Bot does not have perimssion for {ctx.command}",
                timestamp=ctx.message.created_at
            )
            bmpmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=bmpmbed)
        elif isinstance(error, discord.Forbidden):
            fmbed = discord.Embed(
                colour=self.bot.color,
                title="Forbidden Error",
                description="If you are the owner of this server, you can't do the commands that will change things for you\nOr maybe the bot's role is not that high (this won't change the concept for you if you are the owner)",
                timestamp=ctx.message.created_at
            )
            fmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=fmbed)
        elif isinstance(error, commands.MissingRequiredArgument):
            mrambed = discord.Embed(
                colour=self.bot.color,
                title="Please pass an argument",
                timestamp=ctx.message.created_at
            )
            mrambed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=mrambed)
        elif isinstance(error, commands.BadArgument):
            bambed = discord.Embed(
                colour=self.bot.color,
                title="Please pass an correct argument",
                timestamp=ctx.message.created_at
            )
            bambed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=bambed)
        elif isinstance(error, commands.CommandOnCooldown):
            cocmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Command {ctx.command} on Cooldown",
                timestamp=ctx.message.created_at
            )
            cocmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=cocmbed)
        elif isinstance(error, commands.PrivateMessageOnly):
            pmombed = discord.Embed(
                colour=self.bot.color,
                title=F"{ctx.command} can only be used in DMs",
                timestamp=ctx.message.created_at
            )
            pmombed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=pmombed)
        elif isinstance(error, commands.NoPrivateMessage):
            npmmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Can't use {ctx.command} in DMs",
                timestamp=ctx.message.created_at
            )
            npmmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=npmmbed)
        elif isinstance(error, commands.UserNotFound):
            unfmbed = discord.Embed(
                colour=self.bot.color,
                title="Did not find the user",
                timestamp=ctx.message.created_at
            )
            unfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=unfmbed)
        elif isinstance(error, commands.RoleNotFound):
            rnfmbed = discord.Embed(
                colour=self.bot.color,
                title="Did not find the role",
                timestamp=ctx.message.created_at
            )
            rnfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=rnfmbed)
        elif isinstance(error, commands.CheckFailure):
            cfmbed = discord.Embed(
                colour=self.bot.colors,
                title="You are blacklisted, stop using the commands"
            )
            cfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=cfmbed)
        elif isinstance(error, commands.CheckAnyFailure):
            cafmbed = discord.Embed(
                colour=self.bot.colors,
                title="You are blacklisted, stop using the commands"
            )
            cafmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=cafmbed)
        else:
            tbmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Error in {ctx.command}",
                description=''.join(traceback.format_exception(type(error), error,  error.__traceback__)),
                timestamp=ctx.message.created_at
            )
            tbmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=tbmbed)

def setup(bot):
    bot.add_cog(OnError(bot))
