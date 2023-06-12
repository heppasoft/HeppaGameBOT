import random
import discord
import datetime
import typing as t


class TicTacToeButton(discord.ui.Button["TicTacToeView"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToeView = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return
        
        if interaction.user != view.X and interaction.user != view.O:
            await interaction.response.send_message("Bu oyunnda hamle yapamazsınız. Lütfen oyunun bitmesini bekleyip yeni bir oyun başlatın.", ephemeral=True)
            return
        
        if interaction.user != view.current_player:
            await interaction.response.send_message("Hamle sırası henüz sana gelmedi. Lütfen sıranı bekle!", ephemeral=True)
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = "x"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = "o"
        
        winner = view.check_board_winner()
        
        view.current_player = view.X if view.current_player != view.X else view.O
        content = f"Hamle sırası: {view.current_player.mention}"

        self.disabled = True
        
        if winner is not None:
            if winner == view.X:
                content = f"{view.X.mention} Kazandı!!!!"
            elif winner == view.O:
                content = f"{view.O.mention} Kazandı!!!!"
            
            else:
                content = "Berabere!!!"
            
            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToeView(discord.ui.View):
    children: t.List[TicTacToeButton]
    X: discord.Member
    O: discord.Member

    def __init__(self, p1: discord.Member, p2: discord.Member):
        super().__init__()
        self.X = p1
        self.O = p2
        
        self.current_player = random.choice([self.X, self.O])
        
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        
        self.start_datetime = datetime.datetime.now()

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        mark = "x" if self.current_player == self.X else "o"
        
        for l in self.board:
            if l[0] == mark and l[1] == mark and l[2] == mark:
                return self.current_player
        
        for l in range(3):
            if self.board[0][l] == mark and self.board[1][l] == mark and self.board[2][l] == mark:
                return self.current_player
        
        if self.board[0][0] == mark and self.board[1][1] == mark and self.board[2][2] == mark:
            return self.current_player
        
        if self.board[0][2] == mark and self.board[1][1] == mark and self.board[2][0] == mark:
            return self.current_player
        
        if all(i != 0 for row in self.board for i in row):
            return 0
        
        return None
    
    async def stop_game(self):
        self.stop()
        await self.message.edit("Oyun sonlandırıldı!!!", view=self)