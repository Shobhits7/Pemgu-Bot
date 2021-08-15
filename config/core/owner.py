

import discord
from discord.ext import commands
import datetime
import config.utils.json

class Owner(commands.Cog, name="Owner 👑", description="Only lvlahraam can use these commands"):
    def __init__(self, bot):
        self.bot = bot

    # Logout
    @commands.command(name="logout", aliases=["lt"], help="Only lvlahraam can use this command")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.trigger_typing()
        ltmbed = discord.Embed(
            colour=self.bot.color,
            title="Okay, I'm logging out :wave:",
            timestamp=ctx.message.created_at
        )
        ltmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=ltmbed)
        await self.bot.close()

    # Relog
    @commands.command(name="relog", aliases=["rg"], help="Will Relog the bot")
    @commands.is_owner()
    async def relog(self, ctx):
        await ctx.trigger_typing()
        rgmbed = discord.Embed(
            colour=self.bot.color,
            title="Okay Relogging 👀",
            timestamp=ctx.message.created_at
        )
        rgmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=rgmbed)
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
        gdmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=gdmbed)
    
    # Perms
    @commands.command(name="perms", aliases=["pm"], help="Will show the perms that the bot has in this guild")
    @commands.is_owner()
    async def perms(self, ctx):
        await ctx.trigger_typing()
        pmbed = discord.Embed(colour=self.bot.color, title="Bot Permissions", timestamp=ctx.message.created_at)
        pmbed.add_field(name="Allowed", value="\n".join(perm.replace("_", " ") for perm, val in ctx.guild.me.guild_permissions if val))
        pmbed.add_field(name="Allowed", value="\n".join(perm.replace("_", " ") for perm, val in ctx.guild.me.guild_permissions if not val))
        await ctx.reply(embed=pmbed)

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
        tembed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=tembed)
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
        doblmbed = discord.Embed(
            colour=self.bot.color,
            title="Added user to the blacklist",
            timestamp=ctx.message.created_at
        )
        doblmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if user.id in self.bot.blacklist_ids:
            self.bot.blacklist_ids.remove(user.id)
            return await ctx.reply(embed=unblmbed)
        self.bot.blacklist_ids.append(user.id)
        await ctx.reply(embed=doblmbed)

def setup(bot):
    bot.add_cog(Owner(bot))
