import discord
from discord.ext import commands
from config.utils.aiohttp import session_bytes

class Owner(commands.Cog, description="Only lvlahraam can use these commands"):
    def __init__(self, bot):
        self.bot = bot

    # Delete
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    @commands.is_owner()
    async def delete(self, ctx, amount: int):
        await ctx.trigger_typing()
        cumbed = discord.Embed(
            colour=self.bot.color,
            title=F"Deleted {amount} of bot messages",
        )
        cumbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.channel.purge(limit=amount, check=lambda m: m.author.id == self.bot.user.id)
        await ctx.send(embed=cumbed, delete_after=2.5)
        
    # Logout
    @commands.command(name="logout", aliases=["lt"], help="Will logout the bot")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.trigger_typing()
        ltmbed = discord.Embed(
            colour=self.bot.color,
            title="Okay, I'm logging out :wave:",
            timestamp=ctx.message.created_at
        )
        ltmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=ltmbed)
        await self.bot.close()

    # Relog
    @commands.command(name="relog", aliases=["rg"], help="Will Relog the bot")
    @commands.is_owner()
    async def relog(self, ctx):
        await ctx.trigger_typing()
        rgmbed = discord.Embed(
            colour=self.bot.color,
            title="Okay Relogging :eyes:",
            timestamp=ctx.message.created_at
        )
        rgmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=rgmbed)
        await self.bot.close()
        await self.bot.login()
    
    # Guilds
    @commands.command(name="guilds", aliases=["gd"], help="Will tell the guilds that my bot is joined in")
    @commands.is_owner()
    async def guild(self, ctx):
        await ctx.trigger_typing()
        gdmbed = discord.Embed(
            colour=self.bot.color,
            title="This bot is joined in: ",
            description=F"{len(self.bot.guilds)} Servers",
            timestamp=ctx.message.created_at
        )
        gdmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=gdmbed)
    
    # Perms
    @commands.command(name="perms", aliases=["pm"], help="Will show the perms that the bot has in this guild")
    @commands.is_owner()
    async def perms(self, ctx):
        await ctx.trigger_typing()
        pmbed = discord.Embed(colour=self.bot.color, title="Bot Permissions", timestamp=ctx.message.created_at)
        pmbed.add_field(name="Allowed", value="\n".join(perm.replace("_", " ") for perm, val in ctx.guild.me.guild_permissions if val))
        pmbed.add_field(name="Not Allowed", value="\n".join(perm.replace("_", " ") for perm, val in ctx.guild.me.guild_permissions if not val))
        pmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pmbed)

    # Template
    @commands.command(name="template", aliases=["te"], help="Will give the guild's template")
    @commands.is_owner()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def template(self, ctx):
        await ctx.trigger_typing()
        tembed = discord.Embed(
            colour=self.bot.color,
            title="Please check your DM",
            timestamp=ctx.message.created_at
        )
        tembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=tembed)
        temp = await ctx.guild.templates()
        await ctx.author.send(temp)
    
    # Blacklist
    @commands.command(name="blacklist", aliases=["bl"], help="Will put the given user to blaclist")
    @commands.is_owner()
    async def blacklist(self, ctx, user:commands.UserConverter):
        await ctx.trigger_typing()
        unblmbed = discord.Embed(
            colour=self.bot.color,
            title="Removed the user from the blacklist",
            timestamp=ctx.message.created_at
        )
        unblmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        doblmbed = discord.Embed(
            colour=self.bot.color,
            title="Added user to the blacklist",
            timestamp=ctx.message.created_at
        )
        doblmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        if user.id in self.bot.blacklisted:
            self.bot.blacklisted.remove(user.id)
            return await ctx.send(embed=unblmbed)
        self.bot.blacklisted.append(user.id)
        await ctx.send(embed=doblmbed)

    # Code
    @commands.command(name="code", aliases=["cd"], help="Will give you a preview from your code", usage="<code>")
    @commands.is_owner()
    @commands.bot_has_guild_permissions(attach_files=True)
    async def code(self, ctx, *code):
        await ctx.trigger_typing()
        session = await session_bytes(F"https://carbonnowsh.herokuapp.com/?code={code}&paddingVertical=56px&paddingHorizontal=56px&backgroundImage=none&backgroundImageSelection=none&backgroundMode=color&backgroundColor=rgba(88, 89, 185, 100)&dropShadow=true&dropShadowOffsetY=20px&dropShadowBlurRadius=68px&theme=seti&windowTheme=none&language=auto&fontFamily=Hack&fontSize=16px&lineHeight=133%&windowControls=true&widthAdjustment=true&lineNumbers=true&firstLineNumber=0&exportSize=2x&watermark=false&squaredImage=false&hiddenCharacters=false&name=Hello World&width=680")
        cdmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your preview for the code",
            timestamp=ctx.message.created_at
        )
        cdmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        cdmbed.set_image(url="attachment://code.png")
        await ctx.send(file=discord.File(session, filename="code.png"), embed=cdmbed)

    # Status
    @commands.group(name="status", aliases=["st"], help="Will show the bot's current status", invoke_without_command=True)
    @commands.is_owner()
    async def status(self, ctx):
        await ctx.trigger_typing()
        stmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Bot's current status is",
            description=F"{self.bot.activity} - {self.bot.status}",
            timestamp=ctx.message.created_at
        )
        stmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=stmbed)
    # Status Change
    @status.command(name="change", aliases=["stc"], help="Will change the bot's status to the given text", usage="<text>")
    @commands.is_owner()
    async def status_change(self, ctx, *, text):
        await ctx.trigger_typing()
        await self.bot.change_presence(activity=discord.Game(name=text), status=self.bot.status)
        stcmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Bot's status has been now changed to:",
            description=text,
            timestamp=ctx.message.created_at
        )
        stcmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=stcmbed)
    # Status Reset
    @status.command(name="reset", aliases=["str"], help="Will reset the bot's status")
    @commands.is_owner()
    async def status_reset(self, ctx):
        await ctx.trigger_typing()
        await self.bot.change_presence(activity=self.bot.activity, status=self.bot.status)
        strmbed = discord.Embed(
            colour=self.bot.color,
            title="Resetted the bot's status",
            timestamp=ctx.message.created_at
        )
        strmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=strmbed)

def setup(bot):
    bot.add_cog(Owner(bot))
