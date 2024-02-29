import discord
from discord.ext import commands
import requests
from discord import app_commands
import os
from requests.exceptions import JSONDecodeError

class Narrativo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_narrativo = "http://apibot.orivaldo.net:8000/api/v1/nlp/narrativo/"
        self.token = os.getenv('API_TOKEN')

    async def post_narrativo_resposta(self, matricula: int, sigla: str, numero_gabarito: int, resposta_aluno: str):
        payload = {
            "matricula": matricula,
            "sigla": sigla,
            "numero_gabarito": numero_gabarito,
            "resposta_aluno": resposta_aluno
        }
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        try:
            response = requests.post(self.api_narrativo, json=payload, headers=headers)
            response.raise_for_status()
            
            return True
        except JSONDecodeError:
            return None
        except requests.exceptions.RequestException as e:
            return None
    
    class MyModal(discord.ui.Modal, title="Responder narrativo"):
        def __init__(self, *args, **kwargs):
            self.narrativo_instance = kwargs.pop('narrativo_instance')
            super().__init__(*args, **kwargs)

        matricula = discord.ui.TextInput(label="Matricula", placeholder="Digite sua matricula", min_length=1, max_length=100)
        sigla = discord.ui.TextInput(label="Sigla", placeholder="Digite a sigla", min_length=1, max_length=100)
        numero_gabarito = discord.ui.TextInput(label="Número Gabarito", placeholder="Digite o número do gabarito", min_length=1, max_length=100)
        resposta_aluno = discord.ui.TextInput(label="Resposta do Aluno", placeholder="Digite sua resposta", min_length=1, max_length=100)
        
            
            
    @app_commands.command(name="responder_narrativo", description="Responder a um narrativo")
    async def responder_narrativo_command(self, interaction: discord.Interaction):
        mymodal = self.MyModal(narrativo_instance=self)
        await interaction.response.send_modal(mymodal)
        
async def setup(bot):
    await bot.add_cog(Narrativo(bot))
