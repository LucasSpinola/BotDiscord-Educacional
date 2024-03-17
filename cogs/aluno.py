import discord
from discord.ext import commands
from discord import app_commands
import requests
import os

class Aluno(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_aluno = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/cria_aluno"
        self.api_permissao = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def post_create_student(self, nome: str, matricula: int, turma: str, sub_turma: str):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        data = { "nome": nome, "matricula": matricula, "turma": turma, "sub_turma": sub_turma, "id_discord": '0'}
        response = requests.post(self.api_aluno, json=data, headers=headers)
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
    
    @app_commands.command(name="criaraluno", description="Crie um aluno para o banco de dados")
    async def cria_aluno(self, interaction: discord.Interaction, nome: str, matricula: int, turma: str, sub_turma: str):
        id_user = str(interaction.user.id)
        check_permission = await self.check_permission(id_user)
        if check_permission == True:
            alunos = await self.post_create_student(nome, matricula, turma, sub_turma)
            await interaction.response.send_message(f"Aluno {nome} criado com sucesso!")
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para criar um aluno. ❌")

async def setup(bot):
    await bot.add_cog(Aluno(bot))
