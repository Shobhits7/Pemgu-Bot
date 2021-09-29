import discord, os, sys
from discord.ext import commands

class Owner(commands.Cog, description="Only lvlahraam can use these commands"):
    def __init__(self, bot):
        self.bot = bot

    # Load
    @commands.command(name="load", help="Will load the given cog if it was not already loaded", usage="<cog>")
    @commands.is_owner()
    async def load(self, ctx:commands.Context, *, cog):
        floadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully loaded {cog}.",
            timestamp=ctx.message.created_at
        )
        floadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        bloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{cog} is already loaded.",
            timestamp=ctx.message.created_at
        )
        bloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        try:
            self.bot.load_extension(F"config.core.{cog}")
            await ctx.send(embed=floadmbed)
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(embed=bloadmbed)

    # Unload
    @commands.command(name="unload", help="Will unload the given cog if it was already loaded", usage="<cog>")
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, *, cog):
        funloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully unloaded {cog}.",
            timestamp=ctx.message.created_at
        )
        funloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        bunloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{cog} is not already loaded.",
            timestamp=ctx.message.created_at
        )
        bunloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        try:
            self.bot.unload_extension(F"config.core.{cog}")
            await ctx.send(embed=funloadmbed)
        except commands.ExtensionNotLoaded:
            await ctx.send(embed=bunloadmbed)
  
    # Reload
    @commands.command(name="reload", help="Will reload the given cog", usage="<cog>")
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, *, cog):
        reloadmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully reloaded {cog}.",
            timestamp=ctx.message.created_at
        )
        reloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.reload_extension(F"config.core.{cog}")
        await ctx.send(embed=reloadmbed)

    # ReloadAll
    @commands.command(name="reloadall", help="Will reload every cog")
    @commands.is_owner()
    async def reloadall(self, ctx:commands.Context):
        reloadallmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully reloaded every cog",
            description="Here is the results",
            timestamp=ctx.message.created_at
        )
        reloadallmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        errors = []
        for cog in self.bot.extensions:
            try:
                reloadallmbed.description += F"{cog} | Fine"
                self.bot.reload_extension(cog)
            except Exception as error:
                reloadallmbed.description += F"{cog} | Bad"
                errors.append(error)
        if len(errors) != 0:
           reloadallmbed.description += F"Errors:\n{', '.join(error for error in errors)}"
        await ctx.send(embed=reloadallmbed)

    # Repeat
    @commands.command(name="repeat", help="Will repeat the given commands the amounts of given time", usage="<time> <command>")
    @commands.is_owner()
    async def repeat(self, ctx:commands.Context, time:int, command:str):
        for _ in range(1, time+1):
            await self.bot.get_command(str(command))(ctx)
        await ctx.send(F"Successfully repeated `{command}` - `{time}` times")

    # Logout
    @commands.command(name="logout", aliases=["lt"], help="Will logout the bot")
    @commands.is_owner()
    async def logout(self, ctx:commands.Context):
        ltmbed = discord.Embed(
            colour=self.bot.colour,
            title="Okay, I'm logging out :wave:",
            timestamp=ctx.message.created_at
        )
        ltmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=ltmbed)
        await self.bot.close()

    # Relog
    @commands.command(name="relog", aliases=["rg"], help="Will Relog the bot")
    @commands.is_owner()
    async def relog(self, ctx:commands.Context):
        def restart():
            python = sys.executable
            os.execl(python, python, * sys.argv)
        rgmbed = discord.Embed(
            colour=self.bot.colour,
            title="Okay Relogging :eyes:",
            timestamp=ctx.message.created_at
        )
        rgmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=rgmbed)
        restart()

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
