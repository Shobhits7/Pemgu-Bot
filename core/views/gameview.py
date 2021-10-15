import discord, random
from typing import List

class RPSButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.ctx = view.ctx
        self.botoption = view.botoption
        self.useroption = view.useroption

    async def callback(self, interaction:discord.Interaction):
        if self.label == "Rock":
            self.useroption = "Rock"
        elif self.label == "Paper":
            self.useroption = "Paper"
        elif self.label == "Scissors":
            self.useroption = "Scissors"
        tierpsmbed = discord.Embed(
            color=self.ctx.bot.color,
            description=F"We both chose **{self.botoption}**, It's a tie :|",
            timestamp=interaction.message.created_at
        )
        tierpsmbed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
        wonrpsmbed = discord.Embed(
            color=self.ctx.bot.color,
            description=F"You chose **{self.useroption}**, But, I chose **{self.botoption}**, You won :) / I lost :(",
            timestamp=interaction.message.created_at
        )
        wonrpsmbed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
        lostrpsmbed = discord.Embed(
            color=self.ctx.bot.color,
            description=F"I chose **{self.botoption}**, But, You chose **{self.useroption}**, I won :) / You lost :(",
            timestamp=interaction.message.created_at
        )
        lostrpsmbed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
        if self.useroption == self.botoption:
            self.view.clear_items()
            await interaction.response.edit_message(embed=tierpsmbed, view=self.view)
        else:
            self.view.clear_items()
            if self.useroption == "Rock" and self.botoption == "Scissors" \
               or self.useroption == "Paper" and self.botoption == "Rock" \
                   or self.useroption == "Scissors" and self.botoption == "Paper":
                   await interaction.response.edit_message(embed=wonrpsmbed, view=self.view)
            elif self.useroption == "Scissors" and self.botoption == "Rock" \
                or self.useroption == "Rock" and self.botoption == "Paper" \
                    or self.useroption == "Paper" and self.botoption == "Scissors":
                    await interaction.response.edit_message(embed=lostrpsmbed, view=self.view)

class RPSView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=5)
        self.ctx = ctx
        self.botoption = random.choice(["Rock", "Paper", "Scissors"])
        self.useroption = ""
        self.add_item(item=RPSButtons(emoji="🗻", label="Rock", style=discord.ButtonStyle.green, view=self))
        self.add_item(item=RPSButtons(emoji="🧻", label="Paper", style=discord.ButtonStyle.blurple, view=self))
        self.add_item(item=RPSButtons(emoji="🔪", label="Scissors", style=discord.ButtonStyle.red, view=self))

    async def on_timeout(self):
        if self.children:
            for item in self.children:
                self.clear_items()
                self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.red, disabled=True))
                await self.message.edit(view=self)

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.message.author.id:
            return True
        else:
            icheckmbed = discord.Embed(
                color=self.ctx.bot.color,
                title=F"You can't use this",
                description=F"<@{interaction.user.id}> - Only <@{self.ctx.message.author.id}> can use this\nCause they did the command\nIf you want to use this, do what they did",
                timestamp=interaction.message.created_at
            )
            icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
            return False

class GuessButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.ctx = view.ctx
        self.choose = view.choose
        self.number = view.number
    
    async def callback(self, interaction:discord.Interaction):
        if self.label == self.number:
            self.choose = True
        elif self.label != self.number:
            self.choose = False
        if self.choose == True:
            truembed = discord.Embed(
                color=self.ctx.bot.color,
                title="You guessed correctly",
                description=F"The number was {self.number}"
            )
            truembed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
            self.view.clear_items()
            await interaction.response.edit_message(embed=truembed, view=self.view)
        if self.choose == False:
            falsembed = discord.Embed(
                color=self.ctx.bot.color,
                title="You guessed incorrectly",
                description=F"The correct answer was {self.number}"
            )
            falsembed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
            self.view.clear_items()
            await interaction.response.edit_message(embed=falsembed, view=self.view)

class GuessView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=5)
        self.ctx = ctx
        self.choose = None
        self.number = random.randint(1, 5)
        row = 0
        for _ in range(1, 6):
            row += 1
            if row >= 5:
                row -= 1
            self.add_item(item=GuessButtons(label=_, style=discord.ButtonStyle.green, row=row, view=self))
    
    async def on_timeout(self):
        if self.children:
            for item in self.children:
                self.clear_items()
                self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.red, disabled=True))
                await self.message.edit(view=self)

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.message.author.id:
            return True
        else:
            icheckmbed = discord.Embed(
                color=self.ctx.bot.color,
                title=F"You can't use this",
                description=F"<@{interaction.user.id}> - Only <@{self.ctx.message.author.id}> can use this\nCause they did the command\nIf you want to use this, do what they did",
                timestamp=interaction.message.created_at
            )
            icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
            return False

class TicTacToeButton(discord.ui.Button['TicTacToeView']):
    def __init__(self, x:int, y:int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
    
    async def callback(self, interaction:discord.Interaction):
        assert self.view is not None
        view: TicTacToeView = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)
class TicTacToeView(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None