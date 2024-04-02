import discord
from discord.ext import commands
from discord import app_commands
import requests
import os

API = os.getenv('API_URL')

class Turma(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_turmas = "{API}/api/v1/turmas/ler_turma_professor"
        self.api_permissao = "{API}/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def get_turmas(self, id_professor: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_turmas}/{id_professor}", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}/{id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            api_id_discord = data.get('id', '')
            if api_id_discord == id_discord:
                return True
        return False
    
    
    @app_commands.command(name="minhasturmas", description="Listar turmas do professor!")
    async def listar_turmas(self, interaction: discord.Interaction):
        id_professor = str(interaction.user.id)
        check_permission = await self.check_permission(id_professor)
        if check_permission == True:
            turmas = await self.get_turmas(id_professor)
            if turmas:
                docente = next(iter(turmas.values()), {}).get('docente', 'Não especificado')
                embed = discord.Embed(title=f"Professor: <{interaction.user}>", color=0x0000FF)
                turma_list = '\n'.join(turmas.keys())
                embed.add_field(name="Turmas:", value=turma_list, inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Erro ao obter as turmas do professor! ❌")
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Turma(bot))
