from discord.ext import commands
from discord import app_commands, Embed
import requests
import os
import discord

class Chamada(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/presenca/pegar_frequencia_hoje"
        self.api_permissao = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}/{id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            api_id_discord = data.get('id', '')
            if api_id_discord == id_discord:
                return True
        return False
    
    async def get_attendance(self, sigla: str): 
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_url}/{sigla}", headers=headers)
        if response.status_code == 200:
            return response.json().get('frequencias', {})
        return {}

    @app_commands.command(name="chamada", description="Veja as presenças que foram registradas hoje")
    async def chamada(self, interaction: discord.Interaction, turma: str):
        user_id = str(interaction.user.id)
        check_permission = await self.check_permission(user_id)
        if check_permission:
            frequencias = await self.get_attendance(turma)
            if frequencias:
                embed = Embed(title=f"Frequência - {turma}",description="Presenças cadastradas hoje:", color=0x0000FF)
                for student_id, data in frequencias.items():
                    embed.add_field(name=data['nome'], value='', inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{interaction.user}, não foram encontradas presenças registradas para hoje na turma {turma}. ❌")
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Chamada(bot))
