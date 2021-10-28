import discord
from discord.ext import commands

class Moderation(commands.Cog, description="Was someone being bad?"):
    def __init__(self, bot):
        self.bot = bot

    # Ban
    @commands.command(name="ban", aliases=["bn"], help="Will ban the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx:commands.Context, user:discord.User, *, reason:str=None):
        reason = "Nothing was provided" if not reason else reason
        abnmbed = discord.Embed(
            color=self.bot.color,
            title=F"{user} is now Banned",
            description=F"For reason: {reason}",
            timestamp=ctx.message.created_at
        )
        abnmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        ubnmbed = discord.Embed(
            color=self.bot.color,
            title=F"Dear {user}"
        )
        ubnmbed.add_field(name=F"You were banned from:", value=F"{ctx.guild.id}")
        ubnmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        ubnmbed.add_field(name=F"For this reason:", value=reason)
        ubnmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(embed=abnmbed)

    # Unban
    @commands.command(name="unban", aliases=["un"], help="Will unban the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx:commands.Context, user:discord.User, *, reason:str=None):
        reason = "Nothing was provided" if not reason else reason
        aunmbed = discord.Embed(
            color=self.bot.color,
            title=F"{user} is now Unbanned",
            timestamp=ctx.message.created_at
        )
        aunmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        uunmbed = discord.Embed(
            color=self.bot.color,
            title=F"Dear {user}"
        )
        uunmbed.add_field(name=F"You were unbanned from:", value=F"{ctx.guild.id}")
        uunmbed.add_field(name=F"By:", value=F"{ctx.author.name}")
        uunmbed.add_field(name=F"For this reason:", value=reason)
        uunmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.guild.unban(user)
        await ctx.send(embed=aunmbed)

    # Kick
    @commands.command(name="kick", aliases=["kc"], help="Will kick the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx:commands.Context, member:discord.Member, *, reason:str=None):
        reason = "Nothing was provided" if not reason else reason
        akcmbed = discord.Embed(
            color=self.bot.color,
            title=F"{member} is now Kicked",
            description=F"For reason: {reason}",
            timestamp=ctx.message.created_at
        )
        akcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        ukcmbed = discord.Embed(
            color=self.bot.color,
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
            color=self.bot.color,
            description=F"{member.mention}\n{role.mention}",
            timestamp=ctx.message.created_at
        )
        aembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if role in member.roles:
            aembed.title = "Already has"
            return await ctx.send(embed=aembed)
        aembed.title = "Successfully added"
        await member.add_roles(role)
        await ctx.send(embed=aembed)
    
    # RemoveRole
    @commands.command(name="removerole", aliases=["re"], help="Will remove the given role from the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx:commands.Context, member:discord.Member, role:discord.Role):
        rembed = discord.Embed(
            color=self.bot.color,
            description=F"{member.mention}\n{role.mention}",
            timestamp=ctx.message.created_at
        )
        rembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if role in member.roles:
            rembed.title = "Successfully removed"
            await member.remove_roles(role)
            return await ctx.send(embed=rembed)
        rembed.title = "Doesn't have"
        await ctx.send(embed=rembed)

    # Slowmode
    @commands.command(name="slowmode", aliases=["sm"], help="Will change the slowmode of this or the given channel to the given seconds")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def slowmode(self, ctx:commands.Context, seconds:int=None, channel:discord.TextChannel=None):
        seconds = 0 if not seconds else seconds
        channel = ctx.channel if not channel else channel
        smmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        smmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if channel.slowmode_delay == seconds:
            smmbed.title = "Channel is already at the same slowmode"
            smmbed.description = F"Channel: {channel.mention}\nSeconds: {channel.slowmode_delay}"
            return await ctx.send(embed=smmbed)
        smmbed.title = "Successfully changed the slowdown:"
        smmbed.description = F"Channel: {channel.mention}\nSeconds: {seconds}"
        await channel.edit(reason=F"Channel: {channel.mention}\nSeconds: {seconds}\nBy: {ctx.author}", slowmode_delay=seconds)
        await ctx.send(embed=smmbed)

    # Lock
    @commands.command(name="lock", aliases=["lc"], help="Will lock this or the given channel")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lock(self, ctx:commands.Context, channel:discord.TextChannel=None):
        channel = ctx.channel if not channel else channel
        lcmbed = discord.Embed(
            color=self.bot.color,
            description=channel.mention,
            timestamp=ctx.message.created_at
        )
        lcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        over = channel.overwrites_for(ctx.guild.default_role)
        over.send_messages = False
        over.add_reactions = False
        over.create_public_threads = False
        over.create_private_threads = False
        if not channel.permissions_for(ctx.guild.default_role).send_messages:
            lcmbed.title = "Is already locked:"
            return await ctx.send(embed=lcmbed)
        else:
            lcmbed.title = "Successfully Locked:"
            await channel.set_permissions(ctx.guild.default_role, overwrite=over)
            await ctx.send(embed=lcmbed)

    # UnLock
    @commands.command(name="unlock", aliases=["ulc"], help="Will unlock this or the given channel")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx:commands.Context, channel:discord.TextChannel=None):
        channel = ctx.channel if not channel else channel
        ulcmbed = discord.Embed(
            color=self.bot.color,
            description=channel.mention,
            timestamp=ctx.message.created_at
        )
        ulcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        over = channel.overwrites_for(ctx.guild.default_role)
        over.send_messages = True
        over.add_reactions = True
        over.create_public_threads = True
        over.create_private_threads = True
        if channel.permissions_for(ctx.guild.default_role).send_messages:
            ulcmbed.title = "Is already unlocked:"
            return await ctx.send(embed=ulcmbed)
        else:
            ulcmbed.title = "Successfully Unlocked:"
            await channel.set_permissions(ctx.guild.default_role, overwrite=over)
            await ctx.send(embed=ulcmbed)

    # Mute
    @commands.command(name="mute", aliases=["mt"], help="Will mute or unmute the given user")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True, manage_channels=True)
    async def mute(self, ctx:commands.Context, member:discord.Member, *, reason:str=None):
        reason = "Nothing was provided" if not reason else reason
        mtmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        mtmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        for role in ctx.guild.roles:
            if role.name == "Muted":
                muterole = role
                break
        else:
            muterole = await ctx.guild.create_role(
                color=discord.Color.red(),
                name="Muted",
                mentionable=True,
                reason="There was no Muted role, so I created one."
            )
            crmtmbed = discord.Embed(
                color=self.bot.color,
                title=F"There was no Muted role, so I created one",
                description=muterole.mention,
                timestamp=ctx.message.created_at
            )
            crmtmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=crmtmbed)
            for channel in ctx.guild.channels:
                await channel.set_permissions(muterole, send_messages=False)
        if muterole in member.roles:
            mtmbed.title = F"Successfully Un-Muted"
            mtmbed.description = F"UnMuted: {member.mention}\nReason: {reason}\nRole: {muterole.mention}"
            await member.remove_roles(muterole, reason=F"UnMuted by {ctx.author}, Because: {reason}")
            await ctx.send(embed=mtmbed)
        else:
            mtmbed.title = F"Successfully Muted"
            mtmbed.description = F"Muted: {member.mention}\nReason: {reason}\nRole: {muterole.mention}"
            await member.add_roles(muterole, reason=F"Muted by {ctx.author}, Because: {reason}")
            await ctx.send(embed=mtmbed)

    # Purge
    @commands.command(name="purge", aliases=["pu"], help="Will delete messages with the given amount")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx:commands.Context, *, amount:int):
        pumbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        pumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if amount > 100:
            pumbed.title = "Can't clear more than 100 messages"
            return await ctx.send(embed=pumbed, delete_after=5)
        pumbed.title = F"Deleted {amount} amount of messages"
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=pumbed, delete_after=5)

    # EmojiAdd
    @commands.command(name="emojiadd", aliases=["ea"], help="Will create a emoji based on the given name and image")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_emojis=True)
    @commands.bot_has_guild_permissions(manage_emojis=True)
    async def emoji(self, ctx:commands.Context, name:str):
        eambed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        eambed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if not ctx.message.attachments[0]:
            eambed.title = "You need to provide an image"
            return await ctx.send(embed=eambed)
        eambed.title = "Successfully created Emoji:"
        eambed.description = F":{name}:"
        await ctx.guild.create_custom_emoji(name=name, image=ctx.message.attachments[0].read(), reason=F"Added by: {ctx.author}")
        await ctx.send(embed=eambed)

    # EmojiRemove

def setup(bot):
    bot.add_cog(Moderation(bot))