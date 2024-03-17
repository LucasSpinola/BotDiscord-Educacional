import discord
from discord.ext import commands
import requests
from discord import app_commands
import os
class VerMinitestes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/miniteste/aluno"
        self.api_aluno = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/le_aluno"
        self.token = os.getenv('API_TOKEN')

    async def get_student_info(self, id: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_aluno}/{id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for aluno_id, aluno_data in data.items():
                if aluno_data['id_discord'] == id:
                    return aluno_data['turma'], aluno_data['matricula']
        return None, None
    
    async def get_minitestes_por_matricula(self, turma: str, matricula: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_url}/{turma}/{matricula}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        return None

    @app_commands.command(name="verminitestes", description="Veja quais miniteste já foram respondidos")
    async def verminitestes(self, interaction: discord.Interaction):
        id_discord = str(interaction.user.id)
        turma, matricula = await self.get_student_info(id_discord)
        if matricula is None:
            await interaction.response.send_message(f"❌ {interaction.user}, você não está cadastrado no banco de dados.")
        else:
            mini_respondidos = await self.get_minitestes_por_matricula(turma, matricula)
            embed = discord.Embed(
                title=f"Minitestes: {matricula}",
                description=f"Aqui estão os minitestes respondidos:",
                color=discord.Color.blue()
            )
            if not mini_respondidos:
                embed.add_field(name="❌ Nenhum miniteste respondido encontrado", value="❌ Nenhum miniteste foi respondido por esta matrícula.")
            else:
                for miniteste_numero in range(1, 18):
                    if f"T{miniteste_numero}" in mini_respondidos:
                        embed.add_field(name=f"T{miniteste_numero}", value="OK 🟩")
                    else:
                        embed.add_field(name=f"T{miniteste_numero}", value="N/A 🟥")
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(VerMinitestes(bot))
