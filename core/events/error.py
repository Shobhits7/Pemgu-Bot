import discord, difflib, traceback
from discord.ext import commands
from core.views import dymview

class OnError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandNotFound):
                cmd = ctx.invoked_with
                cmds = [cmd.name for cmd in self.bot.commands]
                matches = difflib.get_close_matches(cmd, cmds)
                matcnfmbed = discord.Embed(
                    colour=self.bot.colour,
                    title=F"Couldn't find command called: {cmd}.",
                    description=F"Maybe you meant:\n{' - '.join([match for match in matches])}",
                    timestamp=ctx.message.created_at
                )
                matcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
                nmatcnfmbed = discord.Embed(
                    colour=self.bot.colour,
                    title=F"Couldn't find command called: {cmd}.",
                    description=F"Use help command to know what command you're looking for",
                    timestamp=ctx.message.created_at
                )
                nmatcnfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
                if len(matches) > 0:
                    view = dymview.DYMView(ctx, matches)
                    view.message = await ctx.send(embed=matcnfmbed)
                else:
                    await ctx.send(embed=nmatcnfmbed)
        else:
            print("".join(traceback.format_exception(type(error), error,  error.__traceback__)))
            errors = {
                commands.NotOwner: "You are not the owner of this bot",
                commands.CommandOnCooldown: F"Command **{ctx.invoked_with}** on Cooldown",
                commands.DisabledCommand: F"**{ctx.invoked_with}** is disabled",
                commands.UserNotFound: "Couldn't find the given user",
                commands.MemberNotFound: "Couldn't find the given member",
                commands.RoleNotFound: "Couldn't find the given role",
                commands.EmojiNotFound: "Couldn't find the the given emoji",
                commands.NSFWChannelRequired: F"**{ctx.invoked_with}** is only possible in NSFW channels",
                commands.PrivateMessageOnly: F"**{ctx.invoked_with}** can only be used in DMs",
                commands.NoPrivateMessage: F"Can't use **{ctx.invoked_with}** in DMs",
                commands.CheckFailure: F"<:shut:744345896912945214> YOU <:shut:744345896912945214> ARE  <:shut:744345896912945214> IN <:shut:744345896912945214> BLACKLIST <:shut:744345896912945214> YOU <:shut:744345896912945214> S-KID/IDIOT\nSAY <:shut:744345896912945214> YOU <:shut:744345896912945214> ARE <:shut:744345896912945214> SORRY <:shut:744345896912945214> {ctx.author.mention}",
                discord.Forbidden: "Your problem is one of the problems mentioned below\n\nYou are the owner of this Server:\nIf you are the owner, and you are trying to use a changing info command, you can't\n\nCouldn't send messages to the user:\nThe user is not accepting messages from the members in here or just have this bot blocked\n\nUser's Position:\nThe user's position is higher than me or you"
            }
            errormbed = discord.Embed(
                colour=self.bot.colour,
                title="❌ There was is a problem ❓",
                description=errors[error] if error in errors else error,
                timestamp=ctx.message.created_at
            )
            errormbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=errormbed)
    
def setup(bot):
    bot.add_cog(OnError(bot))