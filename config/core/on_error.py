import discord, traceback, difflib
from discord.ext import commands

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
            nombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=nombed)
        elif isinstance(error, commands.CommandNotFound):
            cmd = ctx.invoked_with
            cmds = [cmd.name for cmd in self.bot.commands]
            matches = difflib.get_close_matches(cmd, cmds)
            matcnfmbed = discord.Embed(
                colour=self.bot.color,
                title=F"There is no `{cmd}` command",
                description=F"Maybe you meant ".join(match for match in matches),
                timestamp=ctx.message.created_at
            )
            matcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            nmatcnfmbed = discord.Embed(
                colour=self.bot.color,
                title=F"There is no `{cmd}` command",
                description="Use `.w help` command to know what command are there",
                timestamp=ctx.message.created_at
            )
            nmatcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            if len(matches) > 0:
                await ctx.send(embed=matcnfmbed)
            else:
                await ctx.send(embed=nmatcnfmbed)
        elif isinstance(error, commands.MissingPermissions):
            mpmbed = discord.Embed(
                colour=self.bot.color,
                title=F"You don't have permission for {ctx.command}",
                timestamp=ctx.message.created_at
            )
            mpmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=mpmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            bmpmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Bot does not have permission for {ctx.command}",
                timestamp=ctx.message.created_at
            )
            bmpmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=bmpmbed)
        elif isinstance(error, discord.Forbidden):
            fmbed = discord.Embed(
                colour=self.bot.color,
                title="Forbidden Error",
                description="The problem is one of the options down below",
                timestamp=ctx.message.created_at
            )
            fmbed.add_field(name="You are the owner of this server:", value="If you are the owner, and you are trying to use changing command, you can't")
            fmbed.add_field(name="Couldn't send messages to the user", value="The user is not accepting messages from the members in here or just blocked this bot")
            fmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=fmbed)
        elif isinstance(error, commands.MissingRequiredArgument):
            mrambed = discord.Embed(
                colour=self.bot.color,
                title="Please pass an argument",
                timestamp=ctx.message.created_at
            )
            mrambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=mrambed)
        elif isinstance(error, commands.BadArgument):
            bambed = discord.Embed(
                colour=self.bot.color,
                title="Please pass an correct argument",
                timestamp=ctx.message.created_at
            )
            bambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=bambed)
        elif isinstance(error, commands.CommandOnCooldown):
            cocmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Command {ctx.command} on Cooldown",
                timestamp=ctx.message.created_at
            )
            cocmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=cocmbed)
        elif isinstance(error, commands.NSFWChannelRequired):
            nsfwcr = discord.Embed(
                colour=self.bot.color,
                title=F"`{ctx.command}` is only possible in nsfw channels"
            )
            nsfwcr.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=nsfwcr)
        elif isinstance(error, commands.PrivateMessageOnly):
            pmombed = discord.Embed(
                colour=self.bot.color,
                title=F"{ctx.command} can only be used in DMs",
                timestamp=ctx.message.created_at
            )
            pmombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=pmombed)
        elif isinstance(error, commands.NoPrivateMessage):
            npmmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Can't use {ctx.command} in DMs",
                timestamp=ctx.message.created_at
            )
            npmmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=npmmbed)
        elif isinstance(error, commands.UserNotFound):
            unfmbed = discord.Embed(
                colour=self.bot.color,
                title="Did not find the user",
                timestamp=ctx.message.created_at
            )
            unfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=unfmbed)
        elif isinstance(error, commands.RoleNotFound):
            rnfmbed = discord.Embed(
                colour=self.bot.color,
                title="Did not find the role",
                timestamp=ctx.message.created_at
            )
            rnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=rnfmbed)
        elif isinstance(error, commands.CheckFailure):
            await ctx.trigger_typing()
            cfmbed = discord.Embed(
                colour=self.bot.color,
                title="You are blacklisted, stop using the commands",
                timestamp=ctx.message.created_at
            )
            cfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=cfmbed)
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.trigger_typing()
            cafmbed = discord.Embed(
                colour=self.bot.color,
                title="You are blacklisted, stop using the commands",
                timestamp=ctx.message.created_at
            )
            cafmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=cafmbed)
        else:
            tbmbed = discord.Embed(
                colour=self.bot.color,
                title=F"Error in {ctx.command}",
                description="".join(traceback.format_exception(type(error), error,  error.__traceback__)),
                timestamp=ctx.message.created_at
            )
            tbmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=tbmbed)

def setup(bot):
    bot.add_cog(OnError(bot))
