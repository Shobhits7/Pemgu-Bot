import discord, random
from typing import List

class TicTacToeButton(discord.ui.Button['TicTacToeView']):
    def __init__(self, x:int, y:int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
    
    async def callback(self, interaction: discord.Interaction):
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
        
class GuessButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.bot = view.bot
        self.choose = view.choose
        self.number = view.number
    
    async def callback(self, interaction: discord.Interaction):
        if self.label == self.number:
            self.choose = True
        elif self.label != self.number:
            self.choose = False
        if self.choose == True:
            truembed = discord.Embed(
                colour=self.bot.color,
                title="You guessed correctly",
                description=F"The number was {self.number}"
            )
            truembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            self.view.clear_items()
            await interaction.response.edit_message(embed=truembed, view=self.view)
        if self.choose == False:
            falsembed = discord.Embed(
                colour=self.bot.color,
                title="You guessed incorrectly",
                description=F"The correct answer was {self.number}"
            )
            falsembed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
            self.view.clear_items()
            await interaction.response.edit_message(embed=falsembed, view=self.view)

class GuessView(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=5)
        self.bot = bot
        self.ctx = ctx
        self.choose = None
        self.number = random.randint(1, 5)
        for i in range(1, 6):
            self.add_item(item=GuessButtons(label=i, style=discord.ButtonStyle.green, row=1, view=self))
    
    async def on_timeout(self):
        if self.children:
            for item in self.children:
                self.clear_items()
                self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.blurple, disabled=True))
                self.add_item(discord.ui.Button(emoji="❌", label="Disabled due to timeout...", style=discord.ButtonStyle.red, disabled=True))
                await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            icheckmbed = discord.Embed(
                colour=self.bot.color,
                title=F"You can't use this",
                description=F"<@{interaction.user.id}> - Only <@{self.ctx.author.id}> can use this\nCause they did the command\nIf you want to use this, do what they did",
                timestamp=interaction.message.created_at
            )
            icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
            return False