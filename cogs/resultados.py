import discord
from discord.ext import commands
import requests
from discord import app_commands
import os

API = os.getenv('API_URL')

class Resultado(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "{API}/api/v1/miniteste/alunos"
        self.api_permissao = "{API}/api/v1/permissao/pegar_permissao"
        self.api_miniteste = "{API}/api/v1/miniteste/pegar/{teste}"
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
            headers = {'Authorization': f'Bearer {self.token}'}
            teste_id = int(teste)
            response = requests.get(self.api_miniteste.format(teste=teste_id), headers=headers)
            if response.status_code == 200:
                data = response.json()
                pergunta_teste = data["pergunta"]
                respostas_mini = data["resposta"]
                n_teste = data["teste"]
            else:
                await interaction.response.send_message(f"{interaction.user}, este teste não existe ou ocorreu um erro ao recuperar os dados. 🔴")
            alunos = await self.get_miniteste_alunos(turma)
            total_respostas = 0 
            respostas_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0} 

            for aluno_data in alunos.values():
                respostas = aluno_data.get('respostas', {})
                resposta_teste = respostas.get('T'+teste, None)
                if resposta_teste: 
                    respostas_count[resposta_teste] += 1
                    total_respostas += 1 
                
            porcentagens = {}
            for resposta, count in respostas_count.items():
                porcentagens[resposta] = (count / total_respostas) * 100 if total_respostas > 0 else 0

            respostas = "\n".join([f"{respostas_mini[resposta]} - {porcentagem:.2f}%" for resposta, porcentagem in porcentagens.items()])
            total_respostas_str = f"Total de alunos que responderam: {total_respostas}"

            embed = discord.Embed(title=f"Resultado: {pergunta_teste} - Teste {teste}", description=respostas, color=0x0000FF)
            embed.set_footer(text=total_respostas_str)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Resultado(bot))