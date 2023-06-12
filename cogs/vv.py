import random
import modules
import discord
import datetime
import typing as t
from modules import constants
from discord.ext import commands

class VV(modules.MyCog):
    games: dict[int, dict] = {}
    
    def __init__(self, client: modules.MyBot) -> None:
        self.client = client
    
    
    # @commands.group("vv", aliases=["vk"], channels="all")
    # async def vv(self, ctx: commands.Context):
    #     pass
    
    
    # @vv.command("start", aliases=["başlat"], help="Var olan bir lobideki oyunu başlatır.")
    # async def vv_start(self, ctx: commands.Context, vampires_count: int):
    #     lobi_config = self.games.get(ctx.author.voice.channel.id)
        
    #     if lobi_config is None:
    #         embed = modules.create_embed(":x: İşlem Başarısız", "Lobi bulunamadı. Lütfen bir lobi oluşutrurup tekrar deneyin.")
    #         await ctx.send(embed=embed, delete_after=5)
        
    #     if ctx.author.id != lobi_config["moderator"]:
    #         embed = modules.create_embed(":x: İşlem Başarısız", "Bulundunuğuz lobinin Yöneticisi değilsiniz.")
    #         await ctx.send(embed=embed, delete_after=5)
        
    #     panel: modules.vv.GamePanel = lobi_config.get("panel")
    #     vc = ctx.author.voice.channel
    #     category = vc.category
        
    #     for member in vc.members:
    #         if member.id == panel.moderator.id: continue
            
    #         panel.add_player(member.id, member.display_name)
    #         await member.add_roles(modules.get(ctx.guild.roles, id=constants.MUTED_ROLE))
        
    #     panel.start_game(vampires_count)
    #     lobi_config["panel"] = panel
        
    #     i = 0
    #     for v in panel.get_vampires():
    #         i+=1
    #         vampires = modules.get(ctx.guild.members, id=v.id)
    #         overwrites = {
    #             ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
    #             vampires: discord.PermissionOverwrite(read_messages=True)
    #         }
    #         v1tc = await category.create_text_channel(f"Vampir {i}", overwrites=overwrites)
        
    #     self.games[ctx.author.voice.channel.id] = lobi_config
    
    
    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    #     possible_channel_name = f"Vampir - Köylü ({member.display_name})"
        
    #     if after.channel:
    #         if after.channel.id == constants.SERVER_VV_VOICE_CHANNEL_ID:
    #             position = after.channel.category.position
    #             category = await member.guild.create_category(possible_channel_name, position=position)
    #             await category.set_permissions(member.guild.default_role, view_channel=False)
    #             await category.set_permissions(modules.get(member.guild.roles, id=constants.MEMBER_ROLE), view_channel=True)
                
    #             vc = await category.create_voice_channel("Lobi")
    #             await member.move_to(vc)
                
    #             mtc = await category.create_text_channel("Mikrofonsuzlar", overwrites={member.guild.default_role: discord.PermissionOverwrite(send_messages=False)})
                
    #             atc = await category.create_text_channel("Yönetici Paneli")
    #             await atc.set_permissions(modules.get(member.guild.roles, id=constants.MEMBER_ROLE), view_channel=False)
    #             await atc.set_permissions(member, view_channel=True)
                
    #             panel = modules.vv.GamePanel()
    #             panel.set_moderator(member.id, member.display_name)
                
    #             embed = modules.create_embed("Vampir - Köylü Oyun Paneli")
    #             embed.add_field("Vampirler: ", "\n".join(panel.get_vampires()) if len(panel.get_vampires()) else "**----**")
                
    #             panel.content = f"{member.mention} lobinizin Yönetici paneli: "
    #             panel.embed = embed
                
    #             await atc.send(f"{member.mention} lobinizin Yönetici paneli: ", embed=embed, view=panel)
                
    #             self.games[vc.id] = {"category": category.id, "moderator": member.id, "panel": panel, "channels": [atc.id, mtc.id]}
        
    #     if before.channel:
    #         if "Vampir - Köylü (" in before.channel.name or before.channel.id in self.games:
    #             if len(before.channel.members) == 0:
    #                 category: discord.CategoryChannel = modules.get(member.guild.categories, id = self.games[before.channel.id]["category"])
                    
    #                 for channel in category.channels:
    #                     await channel.delete()
                        
    #                 await category.delete()
    #                 del self.games[before.channel.id]
    

def setup(client: modules.MyBot):
    client.add_cog(VV(client))