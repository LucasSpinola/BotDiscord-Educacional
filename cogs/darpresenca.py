from discord.ext import commands
from discord import app_commands
import requests
import os
import discord

class DarPresenca(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_presenca = "http://apibot.orivaldo.pro.br:8000/api/v1/presenca/marcar-presenca/"
        self.api_permissao = "http://apibot.orivaldo.pro.br:8000/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')
        
    async def marcar_presenca(self, sigla: str, matricula: int, data: str):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        data = {"sigla": sigla, "matricula": matricula,"data": data}
        response = requests.post(self.api_presenca, json=data, headers=headers)
        return response
    
    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}/{id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            api_id_discord = data.get('id', '')
            if api_id_discord == id_discord:
                return True
        return False

    @app_commands.command(name="darpresenca", description="Professor da presença ao aluno em uma determidana turma e data. Use o formato YYYY-MM-DD")
    async def registrar_presenca(self, interaction: discord.Interaction, matricula: int, sigla: str, data: str):
        id_user = str(interaction.user.id)
        check_permission = await self.check_permission(id_user)
        
        if check_permission:
            presenca = await self.marcar_presenca(sigla, matricula, data)
            if presenca.status_code == 200:
                response_json = presenca.json()
                if "detail" in response_json and "formato de data inválido. Use o formato YYYY-MM-DD" in response_json["detail"]:
                    mensagem = "formato de data inválido. Use o formato YYYY-MM-DD"
                    await interaction.response.send_message(f"{interaction.user}, {mensagem}! 🔴", ephemeral=True)
                elif "mensagem" in response_json:
                    mensagem = response_json["mensagem"]
                    await interaction.response.send_message(f"{mensagem}! ✅")
                else:
                    mensagem = "Presença registrada com sucesso"
                    await interaction.response.send_message(f"{mensagem}! ✅")
            else:
                await interaction.response.send_message(f"{interaction.user}, turma não encontrada ou não atribuída para este usuário! 🔴", ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)


async def setup(bot):
    await bot.add_cog(DarPresenca(bot))
