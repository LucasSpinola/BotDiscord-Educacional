import discord 
from discord import app_commands

class MyGroup(app_commands.Group):
    @app_commands.command()
    async def lop(self,interaction: discord.Interaction):
        await interaction.response.send_message(f"LOP")
        
    @app_commands.command()
    async def ping(self,interaction: discord.Interaction):
        await interaction.response.send_message(f"pong")
        
async def setup(bot):
    bot.tree.add_command(MyGroup(name="ajuda", description="Comando entrada"))