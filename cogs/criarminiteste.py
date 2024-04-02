from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

API = os.getenv('API_URL')

class CriarMiniteste(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "{API}/api/v1/miniteste/criar"
        self.api_permissao = "{API}/api/v1/permissao/pegar_permissao"
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
    
    async def post_create(self, pergunta: str, resposta: dict, teste: str): 
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"pergunta": pergunta, "resposta": resposta, "teste": teste}
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            return True

    @app_commands.command(name="criarminiteste", description="Crie um miniteste no banco de dados.")
    async def criar_miniteste(self, interaction: discord.Interaction, pergunta: str, resposta_a: str, resposta_b: str, resposta_c: str, resposta_d: str, teste: str):
        user_id = str(interaction.user.id)
        resposta = {"A": resposta_a, "B": resposta_b, "C": resposta_c, "D": resposta_d}
        check_permission = await self.check_permission(user_id)
        if check_permission:
            if await self.post_create(pergunta, resposta, teste):
                await interaction.response.send_message(f"{interaction.user}, o miniteste foi criado com sucesso! ✅")
            else:
                await interaction.response.send_message(f"{interaction.user}, ocorreu um erro ao criar o miniteste! 🔺")
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. 🔺", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(CriarMiniteste(bot))
