import discord, expr, asyncio
from discord.ext import commands
import core.views.confirm as cum

class Utility(commands.Cog, description="Useful stuff that are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # Calculator
    @commands.command(name="calculator", aliases=["calc"], help="Will calculate the given math")
    async def calculator(self, ctx:commands.Context, *, math:str):
        output = expr.evaluate(math)
        calcmbed = discord.Embed(
            color=self.bot.color,
            title="Here is your math:",
            description=F"Input: **{math}**\nOutput: **{output}**",
            timestamp=ctx.message.created_at
        )
        calcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=calcmbed)

    # Cleanup
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    async def cleanup(self, ctx:commands.Context, *, amount:int):
        cumbed = discord.Embed(
            color=self.bot.color,
            title=F"Cleaned-up {amount} of bot messages",
        )
        cumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.channel.purge(limit=amount, check=lambda m: m.author.id == self.bot.user.id)
        await ctx.send(embed=cumbed, delete_after=5)

    # Leave
    @commands.command(name="leave", aliases=["lae"], help="Will make the bot leave")
    @commands.has_guild_permissions(administrator=True)
    async def leave(self, ctx:commands.Context):
        laembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        laembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = cum.Confirm(ctx)
        view.message = await ctx.send(content="Are you sure you want the bot to leave:", view=view)
        await view.wait()
        if view.value:
            laembed.title = F"{self.bot.user} has successfully left"
            await ctx.send(embed=laembed)
            await ctx.me.guild.leave()

    # Remind
    @commands.command(name="remind", aliases=["rm"], help="Will remind you with the given task and seconds")
    async def remind(self, ctx:commands.Context, seconds:int, *, task:str):
        await ctx.send(F"Alright {ctx.author.mention}, in {seconds} seconds:, I will remind you About: **{task}**", allowed_mentions=discord.AllowedMentions(users=True))
        await asyncio.sleep(seconds)
        view = discord.ui.View()
        button = discord.ui.Button(label="Go to original message", url=ctx.message.jump_url)
        view.add_item(item=button)
        await ctx.send(F"{ctx.author.mention} Reminded you, as you said **{discord.utils.format_dt(ctx.message.created_at, style='R')}**, About: **{task}**", view=view, allowed_mentions=discord.AllowedMentions(users=True))

    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    async def afk(self, ctx:commands.Context, *, reason:str=None):
        reason = "You didn't provide anything" if not reason else reason
        afkmbed  = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        afkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        afk = self.bot.afks
        if not afk.get(ctx.author.id):
            afk[ctx.author.id] = {"time":discord.utils.utcnow(), "reason":reason}
            afkmbed.title = "Set your AFK"
            afkmbed.description = F"Reason: **{afk[ctx.author.id]['reason']}**"
            await ctx.send(embed=afkmbed)

    # Notes
    @commands.group(name="notes", aliases=["note"], help="Consider using subcommands", invoke_without_command=True)
    async def notes(self, ctx:commands.Context):
        await ctx.send_help("notes")

    # Notes-List
    @notes.command(name="list", aliases=["="], help="Will show every of your or the given user's notes")
    async def notes_list(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        notelistmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        notelistmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT task FROM notes WHERE user_id=$1", user.id)
        if not notes: 
            notelistmbed.title = F"{user} doesn't have any note"
            return await ctx.send(embed=notelistmbed)
        tasks = []
        counter = 0
        for stuff in notes:
            tasks.append(F"`[#{counter}].` {stuff['task']}\n")
            counter += 1
        notelistmbed.title=F"{user}'s notes:"
        notelistmbed.description="".join(task for task in tasks)
        await ctx.send(embed=notelistmbed)

    # Notes-Add
    @notes.command(name="add", aliases=["+"], help="Will add the given task to your notes")
    async def notes_add(self, ctx:commands.Context, *, task:str):
        noteaddmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        noteaddmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        note = await self.bot.postgres.fetchval("SELECT task FROM notes WHERE task=$1 AND user_id=$2", task, ctx.author.id)
        if note:
            noteaddmbed.title = "Is already in your notes:"
            noteaddmbed.description = F"{task}"
            return await ctx.send(embed=noteaddmbed)
        await self.bot.postgres.execute("INSERT INTO notes(user_name,user_id,task) VALUES($1,$2,$3)", ctx.author.name, ctx.author.id, task)
        noteaddmbed.title = "Successfully added:"
        noteaddmbed.description = F"{task}\n**To your notes**"
        await ctx.send(embed=noteaddmbed)

    # Notes-Remove
    @notes.command(name="remove", aliases=["-"], help="Will remove the given task from your notes")
    async def notes_remove(self, ctx:commands.Context, *, number:int):
        noteremovembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        noteremovembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", ctx.author.id)
        if not notes:
            noteremovembed.title = "You don't have any note"
            return await ctx.send(embed=noteremovembed)
        tasks = []
        for stuff in notes:
            tasks.append(stuff["task"])
        if len(tasks) <= number:
            noteremovembed.title = "Is not in your notes:"
            noteremovembed.description = F"{number}\n**Check your notes**"
            return await ctx.send(embed=noteremovembed)
        note = await self.bot.postgres.fetchval("SELECT task FROM notes WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[number])
        if not note:
            noteremovembed.title = "Is not in your notes:"
            noteremovembed.description = F"{number}\n**Check your notes**"
            return await ctx.send(embed=noteremovembed)
        await self.bot.postgres.execute("DELETE FROM notes WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[number])
        noteremovembed.title = "Successfully removed:"
        noteremovembed.description = F"{tasks[number]}\n**From your notes**"
        await ctx.send(embed=noteremovembed)

    # Notes-Clear
    @notes.command(name="clear", aliases=["*"], help="Will clear your notes")
    async def notes_clear(self, ctx:commands.Context):
        noteclearmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        noteclearmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT task FROM notes WHERE user_id=$1", ctx.author.id)
        if not notes:
            noteclearmbed.title = "You don't have any note"
            return await ctx.send(embed=noteclearmbed)
        view = cum.Confirm(ctx)
        view.message = await ctx.send(content="Are you sure if you want to clear everything:", view=view)
        await view.wait()
        if view.value:
            tasks = []
            for stuff in notes:
                tasks.append(stuff["task"])
            for task in tasks:
                await self.bot.postgres.execute("DELETE FROM notes WHERE task=$1 AND user_id=$2", task, ctx.author.id)
            noteclearmbed.title = "Successfully cleared:"
            noteclearmbed.description = "**Your notes**"
            await ctx.send(embed=noteclearmbed)

def setup(bot):
    bot.add_cog(Utility(bot))