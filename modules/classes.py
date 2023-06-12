import sqlite3
import asyncio
import discord
import modules
import typing as t
from modules import constants
from discord.ext import commands


__all__ = [
    "MyBot",
    "MyCog",
    "MyEmbed",
    "SQLDatabase"
]


class MyBot(commands.Bot):
    db: "SQLDatabase"
    
    def __init__(self,**options):
        self.db = options.pop("database")
        super().__init__(**options)
    
    async def process_commands(self: "MyBot", message: discord.Message):
        if message.author.bot:
            return

        ctx: commands.Context = await self.get_context(message)

        if ctx.command is not None:
            channels = ctx.command.__original_kwargs__.get("channels", [])
            
            if isinstance(channels, list) and len(channels) == 0:
                channels = [constants.SERVER_BOT_COMMAND_CHANNEL]
            
            if isinstance(channels, str):
                if channels == "all":
                    channels = []
                else:
                    channels = [channels]
            
            for channel in channels:
                if isinstance(channel, str):
                    channels.append(int(channel))

            if message.channel.id not in channels and len(channels) > 0:
                await message.delete()
                self.dispatch("command_error", ctx, modules.errors.InvalidCommandChannel())
                return

            roles = ctx.command.__original_kwargs__.get("roles", [])
            if not modules.has_ayn_role(message.author, roles) and len(roles) > 0 and not modules.has_ayn_role(message.author, constants.ADMIN_ROLE):
                self.dispatch("command_error", ctx, commands.MissingAnyRole(roles))
                return

        async with ctx.message.channel.typing():
            await self.invoke(ctx)
            await asyncio.sleep(10)


class MyCog(commands.Cog):
    def update_params(self, **kwargs):
        commandds = list(self.__cog_commands__)
        for idx, command in enumerate(commandds):
            for key, val in kwargs.items():
                if key in command.__original_kwargs__:
                    if isinstance(command.__original_kwargs__[key], list):
                        command.__original_kwargs__[key].extend(val)
                        
                    elif isinstance(command.__original_kwargs__[key], dict):
                        command.__original_kwargs__[key].update(val)
                else:
                    command.__original_kwargs__[key] = val
            
            commandds[idx] = command
        self.__cog_commands__ = tuple(commandds)


class MyEmbed(discord.Embed):
    def add_field(self, name: str, value: str, inline: bool = False):
        return super().add_field(name=name, value=value, inline=inline)


class SQLDatabase:
    def __init__(self, db_path: str) -> None:
        self.con = sqlite3.connect(db_path, check_same_thread=False)
    
    def execute(self, sql: str, parameters: set = ()):
        cur = self.con.cursor()
        res = cur.execute(sql, parameters)
        return res
    
    def commit(self):
        self.con.commit()
