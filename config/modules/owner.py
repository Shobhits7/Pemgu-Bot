import discord, os, sys, io, textwrap, traceback, contextlib
from discord.ext import commands

class Owner(commands.Cog, description="Only my Developer can use these commands"):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

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
        loadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully loaded {module}.",
            timestamp=ctx.message.created_at
        )
        loadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.load_extension(F"config.modules.{module}")
        await ctx.send(embed=loadmbed)

    # Unload
    @commands.command(name="unload", help="Will unload the given module if it was already loaded", usage="<module>")
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, *, module:str):
        unloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully unloaded {module}.",
            timestamp=ctx.message.created_at
        )
        unloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.unload_extension(F"config.modules.{module}")
        await ctx.send(embed=unloadmbed)
  
    # Reload
    @commands.group(name="reload", help="Will reload the given  or every module", usage="<module|all>")
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, *, module:str):
        if module == "all":
            allmbed = discord.Embed(
                colour=self.bot.colour,
                title="<:greyTick:596576672900186113> Successfully reloaded every module",
                description="",
                timestamp=ctx.message.created_at
            )
            allmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            errors = []
            for module in self.bot.modules:
                try:
                    self.bot.reload_extension(F"config.modules.{module}")
                    allmbed.description += F"<:greenTick:596576670815879169> - {module}\n"
                except Exception as error:
                    allmbed.description += F"<:redTick:596576672149667840> - {module}\n"
                    errors.append(F"<:redTick:596576672149667840> - {error}\n")
            if len(errors) != 0:
                allmbed.description += ''.join(error for error in errors)
            await ctx.send(embed=allmbed)
        else:
            reunloadmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"Successfully reloaded {module}.",
                timestamp=ctx.message.created_at
            )
            reunloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            self.bot.reload_extension(F"config.modules.{module}")
            await ctx.send(embed=reunloadmbed)
        raise commands.BadArgument

    # Repeat
    @commands.command(name="repeat", help="Will repeat the given commands the amounts of given time", usage="<time> <command>")
    @commands.is_owner()
    async def repeat(self, ctx:commands.Context, time:int, command:str):
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