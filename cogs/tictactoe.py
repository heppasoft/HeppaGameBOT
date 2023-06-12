import modules
import discord
import datetime
import typing as t
from modules import constants
from discord.ext import commands, tasks

class TicTacToe(modules.MyCog):
    tictactoe_view: modules.TicTacToeView = None
    
    def __init__(self, client: modules.MyBot) -> None:
        self.client = client
        self.update_params(channels=[constants.SERVER_TICTACTOE_CHANNEL_ID])
    
    
    @commands.command(name="tictactoe", help="Yeni bir TicTacToe oyunu başlatır.")
    async def tictactoe(self, ctx: commands.Context, p1: discord.Member, p2: t.Optional[discord.Member]):
        if self.tictactoe_view is not None and not self.tictactoe_view.is_finished():
            embed = modules.create_embed(":x: İşlem Başarısız", "Zaten şuanda devam etmekte olan bir oyun bulunmakta. Lütfen oyunun bitmesini bekleyin.")
            await ctx.send(embed=embed, delete_after=5)
            return
        
        p2 = p2 if p2 != None else ctx.message.author
        self.tictactoe_view = modules.TicTacToeView(p1, p2)
        
        await ctx.send(f"Hamle sırası: {self.tictactoe_view.current_player.mention}", view=self.tictactoe_view, reference=ctx.message)
    
    
    @commands.command(name="tictactoe_stop", aliases=["tictactoe_durdur"], help="Devam eden bir TicTacToe oyununu sonlandırır.", roles=[constants.MODERATOR_ROLE])
    async def tictactoe_stop(self, ctx: commands.Context):
        if self.tictactoe_view is None or self.tictactoe_view.is_finished():
            embed = modules.create_embed(":x: İşlem Başarısız", "Devam eden bir oyun bulunmuyor.")
            await ctx.send(embed=embed, delete_after=5)
        else:
            await self.tictactoe_view.stop_game()
            self.tictactoe_view = None
            embed = modules.create_embed(":white_check_mark: İşlem Başarılı", "Devam eden TicTacToe oyununu sonlandırıldı.")
            await ctx.send(embed=embed, delete_after=5)
    
    
    @tasks.loop(minutes=5.0)
    async def check_timeout(self):
        if self.tictactoe_view is not None and not self.tictactoe_view.is_finished():
            td:datetime.timedelta = (datetime.datetime.now() - self.tictactoe_view.start_datetime)
            time_delta = int(divmod(td.total_seconds(), 60)[0])
            if time_delta > 30:
                await self.tictactoe_view.stop_game()
                self.tictactoe_view = None
    
    def cog_unload(self):
        self.check_timeout.cancel()


def setup(client: modules.MyBot):
    client.add_cog(TicTacToe(client))