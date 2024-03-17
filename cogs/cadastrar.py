from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

class Cadastrar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/adicionar_id_discord"
        self.api_aluno = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/le_aluno"
        self.api_permission = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permission}/{id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return 'permissao' in data and data['permissao'].lower() == id_discord.lower()
        return False
    
    async def adicionar_id_discord(self, id_discord: str, matricula: int):
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"matricula": matricula, "id_discord": id_discord}
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if "mensagem" in response_data:
                if response_data["mensagem"] == "Id cadastrado com sucesso":
                    return "success"
                elif response_data["mensagem"] == "O ID Discord já está cadastrado para esta matrícula.":
                    return "already_registered"
        return "error"

    @app_commands.command(name="cadastrar", description="Cadastra seu ID no banco de dados.")
    async def cadastrar_id(self, interaction: discord.Interaction, matricula: int):
        user_id = str(interaction.user.id)
        response = await self.adicionar_id_discord(user_id, matricula)
        if response == "success":
            await interaction.response.send_message(f"{interaction.user}, seu ID foi cadastrado com sucesso! ✅")
        elif response == "already_registered":
            await interaction.response.send_message(f"{interaction.user}, seu ID já foi cadastrado! ❎")
        else:
            await interaction.response.send_message(f"{interaction.user}, ocorreu um erro ao cadastrar seu ID, matricula incorreta ou não cadastrada! 🔴")

async def setup(bot):
    await bot.add_cog(Cadastrar(bot))
