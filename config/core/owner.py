import discord, io
from discord.ext import commands

class Owner(commands.Cog, description="Only lvlahraam can use these commands"):
    def __init__(self, bot):
        self.bot = bot

    # Blacklist
    @commands.command(name="blacklist", aliases=["bl"], help="Will add the given user to the blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx, user:commands.UserConverter):
        await ctx.trigger_typing()
        blacklist = await self.bot.db.fetch("SELECT * FROM blacklist WHERE user_id = $1", user.id)
        blmbed = discord.Embed(
            colour=self.bot.color,
        )
        if len(blacklist) == 0:
            await self.bot.db.execute("INSERT INTO blacklist(user_id) VALUES($1)", user.id)
            blmbed.title = F"Added {user.name} to the blacklist"
        else:
            await self.bot.db.execute("DELETE FROM blacklist WHERE user_id = $1", user.id)
            blmbed.title = F"Removed {user.name} to the blacklist"
        await ctx.send(embed=blmbed)

    # Cleanup
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    @commands.is_owner()
    async def cleanup(self, ctx, amount: int):
        await ctx.trigger_typing()
        cumbed = discord.Embed(
            colour=self.bot.color,
            title=F"Cleaned-up {amount} of bot messages",
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

    # Code
    @commands.command(name="code", aliases=["cd"], help="Will give you a preview from your code", usage="<code>")
    @commands.is_owner()
    @commands.bot_has_guild_permissions(attach_files=True)
    async def code(self, ctx, *code):
        await ctx.trigger_typing()
        async with self.bot.aiosession.get(F"https://carbonnowsh.herokuapp.com/?code={code}&paddingVertical=56px&paddingHorizontal=56px&backgroundImage=none&backgroundImageSelection=none&backgroundMode=color&backgroundColor=rgba(88, 89, 185, 100)&dropShadow=true&dropShadowOffsetY=20px&dropShadowBlurRadius=68px&theme=seti&windowTheme=none&language=auto&fontFamily=Hack&fontSize=16px&lineHeight=133%&windowControls=true&widthAdjustment=true&lineNumbers=true&firstLineNumber=0&exportSize=2x&watermark=false&squaredImage=false&hiddenCharacters=false&name=Hello World&width=680") as response: 
            response = io.BytesIO(await response.read())
        cdmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your preview for the code",
            timestamp=ctx.message.created_at
        )
        cdmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        cdmbed.set_image(url="attachment://code.png")
        await ctx.send(file=discord.File(response, filename="code.png"), embed=cdmbed)

def setup(bot):
    bot.add_cog(Owner(bot))
