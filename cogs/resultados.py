import discord
from discord.ext import commands
import requests
from discord import app_commands
import os

class Resultado(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/miniteste/alunos"
        self.api_permissao = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')
        
    async def get_miniteste_alunos(self, turma: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_url}/{turma}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return {str(i): aluno for i, aluno in enumerate(data, 1)}
            else:
                return data
        return {}
    
    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}/{id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            api_id_discord = data.get('id', '')
            if api_id_discord == id_discord:
                return True
        return False


    @app_commands.command(name="resultadoteste", description="Resultado do miniteste de uma turma!")
    async def resultadosminiteste(self, interaction: discord.Interaction, turma: str, teste: str):
        id_user = str(interaction.user.id)
        check_permission = await self.check_permission(id_user)
        if check_permission == True:
            alunos = await self.get_miniteste_alunos(turma)

            total_alunos_responderam = len(alunos)
            letras_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

            for aluno_data in alunos.values():
                resposta = aluno_data['respostas'].get(teste)
                if resposta in letras_count:
                    letras_count[resposta] += 1

            porcentagens = {}
            for letra, count in letras_count.items():
                porcentagens[letra] = (count / total_alunos_responderam) * 100 if total_alunos_responderam > 0 else 0

            respostas = "\n".join([f"{letra}: {porcentagem:.2f}%" for letra, porcentagem in porcentagens.items()])
            total_alunos_responderam = f"Total de alunos que responderam: {total_alunos_responderam}"

            embed = discord.Embed(title=f"Resultados do miniteste {turma} - Teste {teste}", description=respostas, color=0x0000FF)
            embed.set_footer(text=total_alunos_responderam)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Resultado(bot))
