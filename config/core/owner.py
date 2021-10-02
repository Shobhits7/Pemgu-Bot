import discord, os, sys, io, textwrap, traceback, contextlib
from discord.ext import commands

class Owner(commands.Cog, description="Only my Developer can use these commands"):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command(name='eval', help="Evaluates a code", usage="<body>")
    @commands.is_owner()
    async def _eval(self, ctx, *, body:str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result

        }

        env.update(globals())

        if body.startswith('```') and body.endswith('```'):
            body = '\n'.join(body.split('\n')[1:-1])
        body = body.strip('` \n')
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    # Load
    @commands.command(name="load", help="Will load the given module if it was not already loaded", usage="<module>")
    @commands.is_owner()
    async def load(self, ctx:commands.Context, *, module:str):
        floadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully loaded {module}.",
            timestamp=ctx.message.created_at
        )
        floadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        bloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{module} is already loaded.",
            timestamp=ctx.message.created_at
        )
        bloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        try:
            self.bot.load_extension(F"config.core.{module}")
            await ctx.send(embed=floadmbed)
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(embed=bloadmbed)

    # Unload
    @commands.command(name="unload", help="Will unload the given module if it was already loaded", usage="<module>")
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, *, module:str):
        funloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully unloaded {module}.",
            timestamp=ctx.message.created_at
        )
        funloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        bunloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{module} is not already loaded.",
            timestamp=ctx.message.created_at
        )
        bunloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        try:
            self.bot.unload_extension(F"config.core.{module}")
            await ctx.send(embed=funloadmbed)
        except commands.ExtensionNotLoaded:
            await ctx.send(embed=bunloadmbed)
  
    # Reload
    @commands.group(name="reload", help="Will reload the given module", usage="<module>")
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, *, module:str):
        reloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully reloaded {module}.",
            timestamp=ctx.message.created_at
        )
        reloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.reload_extension(F"config.core.{module}")
        await ctx.send(embed=reloadmbed)

    # ReloadAll
    @commands.command(name="reloadall", help="Will reload every module")
    @commands.is_owner()
    async def reloadall(self, ctx:commands.Context):
        reloadallmbed = discord.Embed(
            colour=self.bot.colour,
            title="<:status_streaming:596576747294818305> Successfully reloaded every module",
            description="<:status_offline:596576752013279242> Here is the results:\n",
            timestamp=ctx.message.created_at
        )
        reloadallmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        errors = []
        toreload = list(self.bot.cogs.keys())
        for module in toreload:
            module = module.lower()
            if module.startswith("on"): module = module[2:]
            try:
                self.bot.reload_extension(F"config.core.{module}")
                reloadallmbed.description += F"<:status_online:596576749790429200> - {module}\n"
            except Exception as error:
                reloadallmbed.description += F"<:status_dnd:596576774364856321> - {module}\n"
                errors.append(F"<:status_idle:596576773488115722> - {error}\n")
        if len(errors) != 0:
           reloadallmbed.description += ''.join(error for error in errors)
        await ctx.send(embed=reloadallmbed)

    # Repeat
    @commands.command(name="repeat", help="Will repeat the given commands the amounts of given time", usage="<time> <command>")
    @commands.is_owner()
    async def repeat(self, ctx:commands.Context, *, time:int, command:str):
        for _ in range(1, time+1):
            await self.bot.get_command(str(command))(ctx)
        await ctx.send(F"Successfully repeated `{command}` - `{time}` times")

    # Shutdown
    @commands.command(name="shutdown",  help="Will shutdown the bot")
    @commands.is_owner()
    async def logout(self, ctx:commands.Context):
        shutdownmbed = discord.Embed(
            colour=self.bot.colour,
            title="I'm shutting-down",
            timestamp=ctx.message.created_at
        )
        shutdownmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=shutdownmbed)
        await self.bot.close()

    # Edit
    @commands.command(name="edit", help="Will change the bot's avatar")
    @commands.is_owner()
    async def edit(self, ctx:commands.Context):
        if not ctx.message.attachments:
            raise commands.MissingRequiredArgument
        for attachment in ctx.message.attachments[0]:
            avatar = io.BytesIO(await attachment.read(use_cached=True))
        editmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully changed bot's avatar",
        )
        editmbed.set_image(url="attachments://avatar.png")
        editmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await self.bot.user.edit(avatar=avatar)
        await ctx.send(file=discord.File(fp=avatar.seek(0), filename="avatar.png"), embed=editmbed)

    # Template
    @commands.command(name="template", aliases=["te"], help="Will give the guild's template")
    @commands.is_owner()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def template(self, ctx:commands.Context):
        tembed = discord.Embed(
            colour=self.bot.colour,
            title="Please check your DM",
            timestamp=ctx.message.created_at
        )
        tembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=tembed)
        temp = await ctx.guild.templates()
        await ctx.author.send(temp)

def setup(bot):
    bot.add_cog(Owner(bot))