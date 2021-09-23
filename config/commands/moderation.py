import discord
from discord.ext import commands

class Moderation(commands.Cog, description="Was someone being bad"):
    def __init__(self, bot):
        self.bot = bot

    # Ban
    @commands.command(name="ban", aliases=["bn"], help="Will ban the user", usage="<user>")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx:commands.Context, user:commands.UserConverter, *, reason=None):
        abnmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} is now Banned",
            description=F"For reason: {reason}",
            timestamp=ctx.message.created_at
        )
        abnmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        ubnmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Dear {user}"
        )
        ubnmbed.add_field(name=F"You were banned from:", value=F"{ctx.guild.id}")
        ubnmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        ubnmbed.add_field(name=F"For this reason:", value=reason)
        ubnmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(embed=abnmbed)

    # Unban
    @commands.command(name="unban", aliases=["un"], help="Will unban the user", usage="<user>")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx:commands.Context, user:commands.UserConverter, *, reason):
        aunmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user.name} is now Unbanned",
            timestamp=ctx.message.created_at
        )
        aunmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        uunmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Dear {user}"
        )
        uunmbed.add_field(name=F"You were unbanned from:", value=F"{ctx.guild.id}")
        uunmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        uunmbed.add_field(name=F"For this reason:", value=reason)
        uunmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.guild.unban(user)
        await ctx.send(embed=aunmbed)

    # Kick
    @commands.command(name="kick", aliases=["kc"], help="Will kick the user", usage="<user>")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx:commands.Context, member:commands.MemberConverter, *, reason=None):
        akcmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{member} is now Kicked",
            description=F"For reason: {reason}",
            timestamp=ctx.message.created_at
        )
        akcmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        ukcmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Dear {member}"
        )
        ukcmbed.add_field(name=F"You were banned from:", value=F"{ctx.guild.id}")
        ukcmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        ukcmbed.add_field(name=F"For this reason:", value=reason)
        ukcmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.guild.kick(user=member, reason=reason)
        await ctx.send(embed=akcmbed)

    # AddRole
    @commands.command(name="addrole", aliases=["ae"], help="Will add the given role to the given user", usage="<user> <role>")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def addrole(self, ctx:commands.Context, member: commands.MemberConverter, role: commands.RoleConverter):
        finaembed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully added the {role} role",
            timestamp=ctx.message.created_at
        )
        finaembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        badaembed = discord.Embed(
            colour=self.bot.colour,
            title=F"The member already has the {role} role",
            timestamp=ctx.message.created_at
        )
        badaembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        if role in member.roles:
            await ctx.send(embed=badaembed)
            return
        await member.add_roles(role)
        await ctx.send(embed=finaembed)
    
    # RemoveRole
    @commands.command(name="removerole", aliases=["re"], help="Will remove the given role from the given user", usage="<user> <role>")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx:commands.Context, member: commands.MemberConverter, role: commands.RoleConverter):
        finrembed = discord.Embed(
            colour=self.bot.colour,
            title=F"Successfully removed the {role} role",
            timestamp=ctx.message.created_at
        )
        finrembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        badrembed = discord.Embed(
            colour=self.bot.colour,
            title=F"The member don't have the {role} role",
            timestamp=ctx.message.created_at
        )
        badrembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(embed=finrembed)
            return
        await ctx.send(embed=badrembed)

    # Purge
    @commands.command(name="purge", aliases=["pu"], help="Will delete messages", usage="<amount>")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx:commands.Context, amount: int):
        finpumbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Deleted {amount} amount of messages",
            timestamp=ctx.message.created_at
        )
        finpumbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        badpumbed = discord.Embed(
            colour=self.bot.colour,
            title="Can't clear more than 100 messages",
            timestamp=ctx.message.created_at
        )
        badpumbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        if amount > 100:
            return await ctx.send(embed=badpumbed, delete_after=2.5)
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=finpumbed, delete_after=2.5)

def setup(bot):
    bot.add_cog(Moderation(bot))
