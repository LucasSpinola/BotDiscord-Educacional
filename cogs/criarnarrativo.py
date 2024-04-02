from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

API = os.getenv('API_URL')

class CriarNarrativo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "{API}/api/v1/narrativo/adicionar"
        self.api_aluno = "{API}/api/v1/alunos/le_aluno"
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
    
    async def post_create(self, pergunta: str, texto_base: str, numero: int): 
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"pergunta": pergunta, "texto_base": texto_base, "numero": numero}
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            return True

    @app_commands.command(name="criarnarrativo", description="Crie um algoritmo de linguagem narrativa no banco de dados.")
    async def criar_narrativo(self, interaction: discord.Interaction, pergunta: str, texto_base: str, numero: int):
        user_id = str(interaction.user.id)
        check_permission = await self.check_permission(user_id)
        if check_permission == True:
            narrativo = await self.post_create(pergunta, texto_base, numero)
            if narrativo:
                await interaction.response.send_message(f"{interaction.user}, o narrativo foi adicionado com sucesso! ✅")
            else:
                await interaction.response.send_message(f"{interaction.user}, ocorreu um erro ao criar o narrativo! 🔺")
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando! 🔺", ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(CriarNarrativo(bot))
