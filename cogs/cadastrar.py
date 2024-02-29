from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

class Cadastrar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.net:8000/api/v1/alunos/adicionar_id_discord"
        self.api_aluno = "http://apibot.orivaldo.net:8000/api/v1/alunos/le_aluno"
        self.api_permission = "http://apibot.orivaldo.net:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permission}?id_discord={id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return 'permissao' in data and data['permissao'].lower() == id_discord.lower()
        return False
    
    async def adicionar_id_discord(self, id_discord: str, matricula: int):
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"matricula": matricula, "id_discord": id_discord}
        response = requests.post(self.api_url, json=data, headers=headers)
        return response.status_code == 200
    
    @app_commands.command(name="cadastrar", description="Cadastra seu ID no banco de dados.")
    async def cadastrar_id(self, interaction: discord.Interaction, matricula: int):
        user_id = str(interaction.user.id)
        if await self.adicionar_id_discord(user_id, matricula):
            await interaction.response.send_message(f"{interaction.user}, seu ID foi cadastrado com sucesso! ✅")
        else:
            await interaction.response.send_message(f"{interaction.user}, ocorreu um erro ao cadastrar seu ID. ❌")
        
async def setup(bot):
    await bot.add_cog(Cadastrar(bot))
