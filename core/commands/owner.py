import discord, io, textwrap, contextlib, traceback
from discord.ext import commands

class Owner(commands.Cog, description="Only my Developer can use these commands"):
    def __init__(self, bot):
        self.bot = bot

    # Eval
    @commands.command(name="eval", help="Evaluates a code")
    @commands.is_owner()
    async def _eval(self, ctx, *, body:str):
        env = {
            "self": self,
            "discord": discord,
            "bot": self.bot,
            "ctx": ctx,
            "message": ctx.message,
            "author": ctx.author,
            "guild": ctx.guild,
            "channel": ctx.channel,
        }
        env.update(globals())
        if body.startswith("```") and body.endswith("```"):
            body = "\n".join(body.split("\n")[1:-1])
        body = body.strip("` \n")
        stdout = io.StringIO()
        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass
            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                await ctx.send(f"```py\n{value}{ret}\n```")

    # Load
    @commands.command(name="load", help="Will load the given cog if it was not already loaded")
    @commands.is_owner()
    async def load(self, ctx:commands.Context, *, cog:str):
        loadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully loaded {cog}.",
            timestamp=ctx.message.created_at
        )
        loadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.load_extension(F"core.{cog}")
        await ctx.send(embed=loadmbed)

    # Unload
    @commands.command(name="unload", help="Will unload the given cog if it was already loaded")
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, *, cog:str):
        unloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully unloaded {cog}.",
            timestamp=ctx.message.created_at
        )
        unloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.unload_extension(F"core.{cog}")
        await ctx.send(embed=unloadmbed)
  
    # Reload
    @commands.command(name="reload", help="Will reload the given  or every cog")
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, *, cog:str):
        if cog in ("all", "every"):
            allmbed = discord.Embed(
                colour=self.bot.colour,
                title="Successfully reloaded every cog",
                description="",
                timestamp=ctx.message.created_at
            )
            allmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            errors = []
            allmbed.description += F"<:greyTick:596576672900186113> Commands:\n"
            for command in self.bot._commands:
                try:
                    self.bot.reload_extension(F"core.commands.{command}")
                    allmbed.description += F"<:greenTick:596576670815879169> - {command}\n"
                except Exception as error:
                    allmbed.description += F"<:redTick:596576672149667840> - {command}\n"
                    errors.append(F"<:redTick:596576672149667840> - {error}\n")
            allmbed.description += F"<:greyTick:596576672900186113> Events:\n"
            for event in self.bot._events:
                try:
                    self.bot.reload_extension(F"core.events.{event}")
                    allmbed.description += F"<:greenTick:596576670815879169> - {event}\n"
                except Exception as error:
                    allmbed.description += F"<:redTick:596576672149667840> - {event}\n"
                    errors.append(F"<:redTick:596576672149667840> - {error}\n")
            if len(errors) != 0:
                allmbed.description += "".join(error for error in errors)
            return await ctx.send(embed=allmbed)
        reunloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully reloaded {cog}.",
            timestamp=ctx.message.created_at
        )
        reunloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.reload_extension(F"core.{cog}")
        await ctx.send(embed=reunloadmbed)

    # Toggle
    @commands.command(name="toggle", help="Will toggle on and off the given command")
    @commands.is_owner()
    async def toggle(self, ctx:commands.Context, command:str):
        command = self.bot.get_command(command)
        if not command.enabled:
            command.enabled = True
            await ctx.send(F"Enabled {command.name} command")
        else:
            command.enabled = False
            await ctx.send(F"Disabled {command.name} command.")

    # Repeat
    @commands.command(name="repeat", help="Will repeat the given commands the amounts of given time")
    @commands.is_owner()
    async def repeat(self, ctx:commands.Context, time:int, command:str):
        for _ in range(1, time+1):
            await self.bot.process_commands(command)
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

    # Blacklist
    @commands.command(name="blacklist", help="Will put the given user to blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx:commands.Context, user:discord.User):
        blacklisted = await self.bot.postgres.fetchval("SELECT user_id FROM blacklist WHERE user_id=$1", user.id)
        blacklistmbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        blacklistmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if not blacklisted:
            await self.bot.postgres.execute("INSERT INTO blacklist(user_name,user_disc,user_id) VALUES($1,$2,$3)", user.name, user.discriminator, user.id)
            blacklistmbed.title = F"Added {user} to blacklist"
        else:
            await self.bot.postgres.execute("DELETE FROM blacklist WHERE user_id=$1", user.id)
            blacklistmbed.title = F"Removed {user} from blacklist"
        await ctx.send(embed=blacklistmbed)

    # Screenshot
    @commands.command(name="screenshot", aliases=["ss"], help="Will give you a preview from the given website")
    @commands.is_owner()
    @commands.bot_has_guild_permissions(attach_files=True)
    async def screenshot(self, ctx:commands.Context, *, website:str):
        session = await self.bot.session.get(F"https://api.screenshotmachine.com?key=a95edd&url={website}&dimension=1024x768")
        response = io.BytesIO(await session.read())
        session.close()
        ssmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is your screenshot",
            timestamp=ctx.message.created_at
        )
        ssmbed.set_image(url="attachment://screenshot.png")
        ssmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(fp=response, filename="screenshot.png"), embed=ssmbed)

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
