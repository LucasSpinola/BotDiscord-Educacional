from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

class Permissao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/adicionar/"
        self.api_aluno = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/le_aluno"
        self.api_permissao = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}/{id_discord}", headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            api_id_discord = data.get('id', '')
            if api_id_discord == id_discord:
                return True
        return False
    
    async def post_create(self, id: str, nome: str, cargo: str): 
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"id": id, "nome": nome, "cargo": cargo}
        response = requests.post(self.api_url, json=data, headers=headers, verify=False)
        if response.status_code == 200:
            return True

    @app_commands.command(name="darpermissao", description="Dar permissão para um usuário.")
    async def criar_pergunta(self, interaction: discord.Interaction, id: str, nome: str, cargo: str):
        user_id = str(interaction.user.id)
        check_permission = await self.check_permission(user_id)
        if check_permission == True:
            if await self.post_create(id, nome, cargo):
                await interaction.response.send_message(f"{interaction.user}, a permissão foi adicionada com sucesso! ✅")
            else:
                await interaction.response.send_message(f"{interaction.user}, ocorreu um erro ao criar a pergunta! 🔴")
        
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. 🔴", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Permissao(bot))
