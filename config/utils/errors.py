import discord, difflib, traceback
from discord.ext import commands
from config.views import dymview

async def handler(bot, ctx, error):
    if isinstance(error, commands.NotOwner):
        nombed = discord.Embed(
            colour=bot.color,
            title="You are not the owner of this bot",
            timestamp=ctx.message.created_at
        )
        nombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=nombed)
    elif isinstance(error, commands.CommandNotFound):
        cmd = ctx.invoked_with
        cmds = [cmd.name for cmd in bot.commands]
        matches = difflib.get_close_matches(cmd, cmds)
        matcnfmbed = discord.Embed(
            colour=bot.color,
            title=F"Couldn't find command called: {cmd}.",
            description=F"Maybe you meant:\n{' - '.join([match for match in matches])}\nClick on the buttons for execution",
            timestamp=ctx.message.created_at
        )
        matcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        nmatcnfmbed = discord.Embed(
            colour=bot.color,
            title=F"Couldn't find command called: {cmd}.",
            description=F"Use help command to know what command you're looking for",
            timestamp=ctx.message.created_at
        )
        nmatcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        if len(matches) > 0:
            view = dymview.DYMView(bot=bot, ctx=ctx.message, matches=matches)
            view.message = await ctx.send(embed=matcnfmbed, view=view)
        else:
            await ctx.send(embed=nmatcnfmbed)
    elif isinstance(error, commands.MissingPermissions):
        mpmbed = discord.Embed(
            colour=bot.color,
            title=F"You don't have permission for {ctx.invoked_with}",
            timestamp=ctx.message.created_at
        )
        mpmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=mpmbed)
    elif isinstance(error, commands.BotMissingPermissions):
        bmpmbed = discord.Embed(
            colour=bot.color,
            title=F"Bot does not have permission for {ctx.invoked_with}",
            timestamp=ctx.message.created_at
        )
        bmpmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=bmpmbed)
    elif isinstance(error, discord.Forbidden):
        fmbed = discord.Embed(
            colour=bot.color,
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
            colour=bot.color,
            title="Please pass an argument",
            timestamp=ctx.message.created_at
        )
        mrambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=mrambed)
    elif isinstance(error, commands.BadArgument):
        bambed = discord.Embed(
            colour=bot.color,
            title="Please pass an correct argument",
            timestamp=ctx.message.created_at
        )
        bambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=bambed)
    elif isinstance(error, commands.CommandOnCooldown):
        cocmbed = discord.Embed(
            colour=bot.color,
            title=F"Command {ctx.invoked_with} on Cooldown",
            timestamp=ctx.message.created_at
        )
        cocmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=cocmbed)
    elif isinstance(error, commands.NSFWChannelRequired):
        nsfwcr = discord.Embed(
            colour=bot.color,
            title=F"{ctx.invoked_with} is only possible in NSFW channels"
        )
        nsfwcr.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=nsfwcr)
    elif isinstance(error, commands.PrivateMessageOnly):
        pmombed = discord.Embed(
            colour=bot.color,
            title=F"{ctx.invoked_with} can only be used in DMs",
            timestamp=ctx.message.created_at
        )
        pmombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pmombed)
    elif isinstance(error, commands.NoPrivateMessage):
        npmmbed = discord.Embed(
            colour=bot.color,
            title=F"Can't use {ctx.invoked_with} in DMs",
            timestamp=ctx.message.created_at
        )
        npmmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=npmmbed)
    elif isinstance(error, commands.UserNotFound):
        unfmbed = discord.Embed(
            colour=bot.color,
            title="Did not find the user",
            timestamp=ctx.message.created_at
        )
        unfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=unfmbed)
    elif isinstance(error, commands.RoleNotFound):
        rnfmbed = discord.Embed(
            colour=bot.color,
            title="Did not find the role",
            timestamp=ctx.message.created_at
        )
        rnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=rnfmbed)
    else:
        tbmbed = discord.Embed(
            colour=bot.color,
            title=F"Error in {ctx.command}",
            description="```py\n",
            timestamp=ctx.message.created_at
        )
        tbmbed.description += F"{''.join(traceback.format_exception(type(error), error,  error.__traceback__))}\n```"
        
        await ctx.send(embed=tbmbed)