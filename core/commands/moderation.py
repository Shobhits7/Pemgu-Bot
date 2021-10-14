import discord
from discord.ext import commands

class Moderation(commands.Cog, description="Was someone being bad?"):
    def __init__(self, bot):
        self.bot = bot

    # Ban
    @commands.command(name="ban", aliases=["bn"], help="Will ban the user")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx:commands.Context, user:discord.User, *, reason:str=None):
        abnmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} is now Banned",
            description=F"For reason: {reason}",
            timestamp=ctx.message.created_at
        )
        abnmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        ubnmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Dear {user}"
        )
        ubnmbed.add_field(name=F"You were banned from:", value=F"{ctx.guild.id}")
        ubnmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        ubnmbed.add_field(name=F"For this reason:", value=reason)
        ubnmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(embed=abnmbed)

    # Unban
    @commands.command(name="unban", aliases=["un"], help="Will unban the user")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx:commands.Context, user:discord.User, *, reason:str=None):
        aunmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} is now Unbanned",
            timestamp=ctx.message.created_at
        )
        aunmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        uunmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Dear {user}"
        )
        uunmbed.add_field(name=F"You were unbanned from:", value=F"{ctx.guild.id}")
        uunmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        uunmbed.add_field(name=F"For this reason:", value=reason)
        uunmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.guild.unban(user)
        await ctx.send(embed=aunmbed)

    # Kick
    @commands.command(name="kick", aliases=["kc"], help="Will kick the user")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx:commands.Context, member:discord.Member, *, reason:str=None):
        akcmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{member} is now Kicked",
            description=F"For reason: {reason}",
            timestamp=ctx.message.created_at
        )
        akcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        ukcmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Dear {member}"
        )
        ukcmbed.add_field(name=F"You were banned from:", value=F"{ctx.guild.id}")
        ukcmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        ukcmbed.add_field(name=F"For this reason:", value=reason)
        ukcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.guild.kick(user=member, reason=reason)
        await ctx.send(embed=akcmbed)

    # AddRole
    @commands.command(name="addrole", aliases=["ae"], help="Will add the given role to the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def addrole(self, ctx:commands.Context, member:discord.Member, role:discord.Role):
        aembed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        aembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if role in member.roles:
            aembed.title = F"The member already has the {role} role"
            return await ctx.send(embed=aembed)
        aembed.title = F"Successfully added the {role} role"
        await member.add_roles(role)
        await ctx.send(embed=aembed)
    
    # RemoveRole
    @commands.command(name="removerole", aliases=["re"], help="Will remove the given role from the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx:commands.Context, member:discord.Member, role:discord.Role):
        rembed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        rembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if role in member.roles:
            rembed.title = F"Successfully removed the {role} role"
            await member.remove_roles(role)
            return await ctx.send(embed=rembed)
        rembed.title = F"The member doesn't have the {role} role"
        await ctx.send(embed=rembed)

    # Lock
    @commands.command(name="lock", aliases=["lc"], help="Will lock the given channel", hidden=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lock(self, ctx:commands.Context, channel:discord.TextChannel=None):
        channel = ctx.channel if not channel else channel
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)}
        lcmbed = discord.Embed(
            colour=self.bot.colour,
            description=channel.mention,
            timestamp=ctx.message.created_at
        )
        lcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if channel.overwrites == overwrites:
            lcmbed.title = "Is already locked:"
            return await ctx.send(embed=lcmbed)
        lcmbed.title = "Successfully Locked:"
        await channel.edit(overwrites=overwrites)
        await ctx.send(embed=lcmbed)

    # Unlock
    @commands.command(name="unlock", aliases=["ulc"], help="Will unlock the given channel", hidden=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx:commands.Context, channel:discord.TextChannel=None):
        channel = ctx.channel if not channel else channel
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)}
        ulcmbed = discord.Embed(
            colour=self.bot.colour,
            description=channel.mention,
            timestamp=ctx.message.created_at
        )
        ulcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if channel.overwrites == overwrites:
            ulcmbed.title = "Is already unlocked:"
            return await ctx.send(embed=ulcmbed)
        ulcmbed.title = "Successfully Unlocked:"
        await channel.edit(overwrites=overwrites)
        await ctx.send(embed=ulcmbed)

    # Mute
    @commands.command(name="mute", aliases=["mt"], help="Will mute the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def mute(self, ctx:commands.Context, member:discord.Member, *, reason:str=None):
        mtmbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        mtmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        for role in ctx.guild.roles:
            if role.name == "Muted" and role.color == discord.Colour.red():
                muterole = role
                break
        else:
            muterole = await ctx.guild.create_role(
                colour=discord.Colour.red(),
                name="Muted",
                mentionable=True,
                reason="There was no Muted role, so I created one."
            )
            crmtmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"There was no Muted role, so I created one",
                timestamp=ctx.message.created_at
            )
            crmtmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.send(content=muterole.mention, embed=crmtmbed)
            for channel in ctx.guild.channels:
                if not channel.permissions_synced:
                    await channel.set_permissions(muterole, add_reactions=False, connect=False, speak=False, stream=False, send_messages=False, send_messages_in_threads=False, send_tts_messages=False, create_instant_invite=False, create_public_threads=False, create_private_threads=False)
        if muterole in member.roles:
            mtmbed.title = F"Successfully Un-Muted"
            mtmbed.description = F"UnMuted: {member.mention}\nReason: {reason}"
            await member.remove_roles(muterole, reason=F"UnMuted by {ctx.author}, Because: {reason}")
            await ctx.send(embed=mtmbed)
        else:
            mtmbed.title = F"Successfully Muted"
            mtmbed.description = F"Muted: {member.mention}\nReason: {reason}"
            await member.add_roles(muterole, reason=F"Muted by {ctx.author}, Because: {reason}")
            await ctx.send(embed=mtmbed)

    # Purge
    @commands.command(name="purge", aliases=["pu"], help="Will delete messages")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx:commands.Context, *, amount:int):
        pumbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        pumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if amount > 100:
            pumbed.title = "Can't clear more than 100 messages"
            return await ctx.send(embed=pumbed, delete_after=5)
        pumbed.title = F"Deleted {amount} amount of messages"
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=pumbed, delete_after=5)

def setup(bot):
    bot.add_cog(Moderation(bot))