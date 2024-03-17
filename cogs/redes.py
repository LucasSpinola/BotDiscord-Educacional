import discord
from discord.ext import commands
from discord import app_commands

class ButtonsTwo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Youtube", style=discord.ButtonStyle.red, custom_id="5")
    async def redes1(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_message(content="Canal do professor: http://www.youtube.com/@orivaldo 🟥")
    
    @discord.ui.button(label="Email", style=discord.ButtonStyle.blurple, custom_id="6")
    async def redes2(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_message(content="Email do professor: orivaldo@gmail.com 📨")
    
    @discord.ui.button(label="Github", style=discord.ButtonStyle.green, custom_id="7")
    async def redes3(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_message(content="Github do professor: http://github.com/orivaldosantana/ECT2203LoP 🐱‍👤")

class Redes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="redes", description="Redes sociais do professor!")
    async def redes(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Aqui estão as redes sociais do professor Orivaldo!", color=0x0000FF)
        await interaction.response.send_message(embed=embed, view=ButtonsTwo())

async def setup(bot):
    await bot.add_cog(Redes(bot))
