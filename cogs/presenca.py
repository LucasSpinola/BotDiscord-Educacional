from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

API = os.getenv('API_URL')

class Presenca(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "{API}/api/v1/presenca/"
        self.api_aluno = "{API}/api/v1/alunos/le_aluno"
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
                if "detail" in response_json and "fora do intervalo de tempo" in response_json["detail"]:
                    mensagem = "Fora do intervalo de tempo para registrar a presença"
                    await interaction.response.send_message(f"{interaction.user}, {mensagem}! 🔺")
                elif "mensagem" in response_json:
                    mensagem = response_json["mensagem"]
                    await interaction.response.send_message(f"{mensagem}! ✅")
                else:
                    mensagem = "Presença registrada com sucesso"
                    await interaction.response.send_message(f"{mensagem}! ✅")
            else:
                response_json = response.json()
                if "detail" in response_json:
                    mensagem = response_json["detail"]
                else:
                    mensagem = "Erro ao registrar a presença"
                await interaction.response.send_message(f"{interaction.user}, {mensagem}! 🔺")
        else:
            await interaction.response.send_message(f"{interaction.user}, turma não encontrada ou não atribuída para este usuário! 🔺", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Presenca(bot))