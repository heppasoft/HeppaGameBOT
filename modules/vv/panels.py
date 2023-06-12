import random
import discord
import datetime
import typing as t
from .game import *
import modules
from discord.ext import commands

class GamePanelButton(discord.ui.Button["GamePanel"]):
    def __init__(self, *, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None

class GamePanel(discord.ui.View, Game):
    game: Game = None
    started: bool =  False
    __embed: modules.MyEmbed = None
    __content: str = ""
    
    
    def __init__(self):
        super().__init__()
        
        self.game = Game()
    
    
    @property
    def content(self):
        return self.__content
    
    
    @content.setter
    def content(self, content: str):
        self.__content = content
    
    
    @property
    def embed(self):
        return self.__embed
    
    
    @embed.setter
    def embed(self, embed: modules.MyEmbed):
        self.__embed = embed
    
    
    @discord.ui.button(label="Oyunu Başlat", custom_id="vv-panel:start-game", style=discord.ButtonStyle.success, row=0)
    async def start_game_b(self, button: discord.ui.Button, interaction: discord.Interaction):
        b: discord.ui.Button = modules.get(self.children, custom_id="vv-panel:start-game")
        
        self.remove_item(b)
        
        self.started = True
        
        await self.update(interaction)
    
    
    # @discord.ui.button(label="Oyunu Durdur", custom_id="vv-panel:stop-game", style=discord.ButtonStyle.danger, row=0)
    # async def stop_game_b(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     pass
    
    
    # @discord.ui.button(label="Gözleri aç", custom_id="vv-panel:open-eyes", style=discord.ButtonStyle.success, row=0)
    # async def open_eyes(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     pass
    
    
    # @discord.ui.button(label="Gözleri kapat", custom_id="vv-panel:close-eyes", style=discord.ButtonStyle.danger, row=0)
    # async def close_eyes(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     pass
    
    
    async def update(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=self.content, embed=self.embed, view=self)


    def check_winner(self):
        return None
    
    
    async def start_game(self):
        ctx: commands.Context = await self.get_context(self.message)
    
    
    async def stop_game(self):
        self.stop()
        await self.message.edit("Oyun sonlandırıldı!!!", view=self)

