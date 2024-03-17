import discord
from discord.ext import commands
from discord import app_commands
import requests
import os

class Pergunta(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_nlp = "https://apibot.orivaldo.pro.br:8000/api/v1/nlp/pergunta"
        self.token = os.getenv('API_TOKEN')

    async def post_awnser(self, id: str, duvida: str):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        data = {"id_discord": id, "mensagem": duvida}
        response = requests.post(self.api_nlp, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    @app_commands.command(name="pergunta", description="Tire suas dúvidas com o Bot!")
    async def pergunta(self, interaction: discord.Interaction, duvida: str):
        id = str(interaction.user.id)
        response = await self.post_awnser(id, duvida)
        if response:
            await interaction.response.send_message(f"Olá {interaction.user}, achei uma resposta para sua dúvida!\n" + response)
        else:
            await interaction.response.send_message(f"{interaction.user}, erro ao processar a pergunta, tente novamente. ❌")

async def setup(bot):
    await bot.add_cog(Pergunta(bot))
