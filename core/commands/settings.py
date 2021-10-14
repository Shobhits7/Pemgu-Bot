import discord
from discord.ext import commands

class Settings(commands.Cog, description="Setting up the bot with these!"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.group(name="prefix", aliases=["pf"], help="Will tell the prefix", invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx:commands.Context):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        pfmbed = discord.Embed(
            color=self.bot.color,
            title=F"My Prefix here is:",
            description=F"> {self.bot.prefix if not prefix else prefix}",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfmbed)

    # Prefix-Change
    @prefix.command(name="change", aliases=["ch"], help="Will change the prefix to the new given text")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def prefix_change(self, ctx:commands.Context, *, text:str):
        pfchmbed = discord.Embed(
            color=self.bot.color,
            title="Successfully changed prefix to:",
            description=F"> {text}",
            timestamp=ctx.message.created_at
        )
        pfchmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if text == self.bot.prefix: await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        else: prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        if not prefix: await self.bot.postgres.execute("INSERT INTO prefixes(guild_name,guild_id,prefix) VALUES ($1,$2,$3)", ctx.guild.name, ctx.guild.id, text)
        else: await self.bot.postgres.execute("UPDATE prefixes SET prefix=$1 WHERE guild_id=$2", text, ctx.guild.id)
        await ctx.send(embed=pfchmbed)

    # Prefix-Reset
    @prefix.command(name="reset", aliases=["rs"], help="Will reset the prefix")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def prefix_reset(self, ctx:commands.Context):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        if prefix: await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        pfrsmbed = discord.Embed(
            color=self.bot.color,
            title="Successfully resetted to:",
            description=F"> {self.bot.prefix}",
            timestamp=ctx.message.created_at
        )
        pfrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfrsmbed)

    # Welcome
    @commands.group(name="welcome", aliases=["wel"], help="Will tell the status for welcome", invoke_without_command=True)
    @commands.guild_only()
    async def welcome(self, ctx:commands.Context):
        welmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        welmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        welcome = await self.bot.postgres.fetchval("SELECT * FROM welcome WHERE guild_id=$1", ctx.guild.id)
        if not welcome:
            welmbed.title = "Welcome is turned off"
        else:
            msg = await self.bot.postgres.fetchval("SELECT msg FROM welcome WHERE guild_id=$1", ctx.guild.id)
            welmbed.title = "Status for welcome"
            welmbed.description = F"> Turned On\n> {msg}"
        await ctx.send(embed=welmbed)

    # Welcome-Change
    @welcome.command(name="change", aliases=["ch"], help="Will turn off or on the welcome")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def welcome_change(self, ctx:commands.Context):
        welchmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        welchmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        welcome = await self.bot.postgres.fetchval("SELECT * FROM welcome WHERE guild_id=$1", ctx.guild.id)
        if not welcome:
            await self.bot.postgres.execute("INSERT INTO welcome(guild_name,guild_id,msg) VALUES($1,$2,$3)", ctx.guild.name, ctx.guild.id, "Welcome to .guild .member")
            welchmbed.title = "Welcome has been turned on"
        else:
            await self.bot.postgres.execute("DELETE FROM welcome WHERE guild_id=$1", ctx.guild.id)
            welchmbed.title = "Welcome has been turned off"
        await ctx.send(embed=welchmbed)

    # Welcome-Message
    @welcome.command(name="message", aliases=["msg"], help="Will change the main welcome message to the new given message, please input .guild and .member")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def welcome_message(self, ctx:commands.Context, *, msg:str):
        welmsgmbed = discord.Embed(
            color=self.bot.color,
            title = "Welcome message has been changed to:",
            description = F"> {msg}",
            timestamp=ctx.message.created_at
        )
        welmsgmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        welcome = await self.bot.postgres.fetchval("SELECT * FROM welcome WHERE guild_id=$1", ctx.guild.id)
        if not welcome:
            await self.bot.postgres.execute("INSERT INTO welcome(guild_name,guild_id,msg) VALUES($1,$2,$3)", ctx.guild.name, ctx.guild.id, msg)
        else:
            await self.bot.postgres.execute("UPDATE welcome SET msg=$1 WHERE guild_id=$2", msg, ctx.guild.id)
        await ctx.send(embed=welmsgmbed)

    # Goodbye
    @commands.group(name="goodbye", aliases=["bye"], help="Will tell the status for goodbye", invoke_without_command=True)
    @commands.guild_only()
    async def goodbye(self, ctx:commands.Context):
        byembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        byembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        goodbye = await self.bot.postgres.fetchval("SELECT * FROM goodbye WHERE guild_id=$1", ctx.guild.id)
        if not goodbye:
            byembed.title = "Goodbye is turned off"
        else:
            msg = await self.bot.postgres.fetchval("SELECT msg FROM goodbye WHERE guild_id=$1", ctx.guild.id)
            byembed.title = "Status for goodbye"
            byembed.description = F"> Turned On\n> {msg}"
        await ctx.send(embed=byembed)

    # Goodbye-Change
    @goodbye.command(name="change", aliases=["ch"], help="Will turn off or on the goodbye")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def goodbye_change(self, ctx:commands.Context):
        byechmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        byechmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        goodbye = await self.bot.postgres.fetchval("SELECT * FROM goodbye WHERE guild_id=$1", ctx.guild.id)
        if not goodbye:
            await self.bot.postgres.execute("INSERT INTO goodbye(guild_name,guild_id,msg) VALUES($1,$2,$3)", ctx.guild.name, ctx.guild.id, "Thank you .member for being here .guild")
            byechmbed.title = "Goodbye has been turned on"
        else:
            await self.bot.postgres.execute("DELETE FROM goodbye WHERE guild_id=$1", ctx.guild.id)
            byechmbed.title = "Goodbye has been turned off"
        await ctx.send(embed=byechmbed)

    # Goodbye-Message
    @goodbye.command(name="message", aliases=["msg"], help="Will change the main goodbye message to the new given message, please input .guild and .member")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def goodbye_message(self, ctx:commands.Context, *, msg:str):
        byemsgmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        byemsgmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        goodbye = await self.bot.postgres.fetchval("SELECT * FROM goodbye WHERE guild_id=$1", ctx.guild.id)
        if not goodbye:
            await self.bot.postgres.execute("INSERT INTO goodbye(guild_name,guild_id,msg) VALUES($1,$2,$3)", ctx.guild.name, ctx.guild.id, msg)
            byemsgmbed.title = "Goodbye message has been changed to:"
            byemsgmbed.description = F"> {msg}"
        else:
            await self.bot.postgres.execute("UPDATE goodbye SET msg=$1 WHERE guild_id=$2", msg, ctx.guild.id)
            byemsgmbed.title = "Goodbye message has been changed to:"
            byemsgmbed.description = F"> {msg}"
        await ctx.send(embed=byemsgmbed)

def setup(bot):
    bot.add_cog(Settings(bot))