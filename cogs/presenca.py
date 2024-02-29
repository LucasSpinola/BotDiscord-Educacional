
from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

class Presenca(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.net:8000/api/v1/presenca/registrar"
        self.api_aluno = "http://apibot.orivaldo.net:8000/api/v1/alunos/le_aluno"
        self.token = os.getenv('API_TOKEN')

    async def get_student_turma(self, id: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_aluno}/{id}", headers=headers)
        for aluno_id, aluno_data in response.json().items():
            if aluno_data['id_discord'] == id:
                return aluno_data['turma'], aluno_data['matricula']
        else:
            return None

    @app_commands.command(name="presenca", description="Registra a presença do aluno.")
    async def registrar_presenca(self, interaction: discord.Interaction):
        turma, matricula = await self.get_student_turma(str(interaction.user.id))
        if turma:
            headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            data = {"matricula": matricula, "sigla": turma}
            response = requests.post(self.api_url, json=data, headers=headers)

            if response.status_code == 200:
                response_json = response.json()
                mensagem = response_json.get("mensagem", "Presença cadastrada com sucesso!")
                await interaction.response.send_message(f"{mensagem} ✅", ephemeral=True)
            else:
                await interaction.response.send_message(f"{interaction.user}, Matrícula do aluno não encontrada para esta disciplina! ❌", ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user}, turma não encontrada ou não atribuída para este usuário! ❌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Presenca(bot))