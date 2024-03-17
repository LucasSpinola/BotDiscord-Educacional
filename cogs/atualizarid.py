from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

class Atualizar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/atualizar_id_discord"
        self.api_aluno = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/le_aluno"
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
    
    async def resetar_id_discord_request(self, matricula: int, id_discord: str):  # Renomeada para evitar conflito de nomes
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"matricula": matricula, "id_discord": id_discord}
        response = requests.patch(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            return True

    @app_commands.command(name="resetarid", description="Reseta o ID do aluno no banco de dados.")
    async def resetar_id(self, interaction: discord.Interaction, matricula: int, id_discord: str):
        user_id = str(interaction.user.id)
        check_permission = await self.check_permission(user_id)
        if check_permission == True:
            if await self.resetar_id_discord_request(matricula, id_discord):  # Correção aqui
                await interaction.response.send_message(f"{interaction.user}, o ID do aluno foi resetado com sucesso! ✅")
            else:
                await interaction.response.send_message(f"{interaction.user}, ocorreu um erro ao resetar o ID. ❌")
        
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Atualizar(bot))
