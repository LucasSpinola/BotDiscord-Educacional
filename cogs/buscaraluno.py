import discord
from discord.ext import commands
from discord import app_commands
import requests
import os

API = os.getenv('API_URL')

class BuscarAluno(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_aluno = "{API}/api/v1/alunos/busca_aluno"
        self.api_permissao = "{API}/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def post_create_student(self, matricula: int):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        response = requests.get(f"{self.api_aluno}/{matricula}", headers=headers)
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
    
    @app_commands.command(name="buscaraluno", description="Crie um aluno para o banco de dados")
    async def busca_aluno(self, interaction: discord.Interaction, matricula: int):
        id_user = str(interaction.user.id)
        check_permission = await self.check_permission(id_user)
        if check_permission == True:
            alunos = await self.post_create_student(matricula)
            if alunos:
                embed = discord.Embed(title="Informações do aluno:", color=0x0000FF)
                for aluno_id, aluno_info in alunos.items():
                    embed.add_field(name="Nome 👤", value=aluno_info.get('nome', 'N/A'), inline=False)
                    embed.add_field(name="ID 🆔", value=aluno_info.get('id_discord', 'N/A'), inline=False)
                    embed.add_field(name="Matrícula 🎓", value=aluno_info.get('matricula', 'N/A'), inline=False)
                    embed.add_field(name="Turma 🗂️", value=aluno_info.get('turma', 'N/A'), inline=False)
                    embed.add_field(name="Sub-Turma 📚", value=aluno_info.get('sub_turma', 'N/A'), inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{interaction.user}, matricula não cadastrada! ❌")
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para criar um aluno. ❌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BuscarAluno(bot))
