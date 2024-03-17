import discord
from discord.ext import commands
import requests
from discord import app_commands
import os
from requests.exceptions import JSONDecodeError

class Narrativo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_narrativo = "https://apibot.orivaldo.pro.br:8000/api/v1/narrativo/ler_pergunta"
        self.api_postnarra = "https://apibot.orivaldo.pro.br:8000/api/v1/nlp/narrativo"
        self.api_aluno = "https://apibot.orivaldo.pro.br:8000/api/v1/alunos/le_aluno"
        self.token = os.getenv('API_TOKEN')

    async def pegar_narrativo(self, numero_gabarito: int):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_narrativo}/{numero_gabarito}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            pergunta = data.get('pergunta', '')
            return pergunta
        return None
    
    async def post_narrativo_resposta(self, matricula: int, sigla: str, numero_gabarito: int, resposta_aluno: str):
        data = {
            "matricula": matricula,
            "sigla": sigla,
            "numero_gabarito": numero_gabarito,
            "resposta_aluno": resposta_aluno
        }
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        try:
            response = requests.post(self.api_postnarra, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except JSONDecodeError:
            return None
        except requests.exceptions.RequestException as e:
            return None

    async def get_student_info(self, id: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_aluno}/{id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for aluno_id, aluno_data in data.items():
                if aluno_data['id_discord'] == id:
                    return aluno_data['turma'], aluno_data['matricula']
        return None, None
    
    class MyModal(discord.ui.Modal, title="Responder narrativo"):
        def __init__(self, *args, **kwargs):
            self.narrativo_instance = kwargs.pop('narrativo_instance')
            self.pergunta = kwargs.pop('pergunta')
            self.numero_gabarito = kwargs.pop('numero_gabarito')
            super().__init__(*args, **kwargs)
            self.pergunta_input = discord.ui.TextInput(label=self.pergunta, placeholder="Digite a resposta", min_length=1, max_length=100)
            self.add_item(self.pergunta_input)

        async def on_submit(self, interaction: discord.Interaction):
            aluno_id = str(interaction.user.id)
            turma, matricula = await self.narrativo_instance.get_student_info(aluno_id)
            if turma is None or matricula is None:
                await interaction.response.send_message("Não foi possível obter as informações do aluno.", ephemeral=True)
                return
            resposta_aluno = self.pergunta_input.value
            response = await self.narrativo_instance.post_narrativo_resposta(matricula, turma, self.numero_gabarito, resposta_aluno)
            if response and 'mensagem' in response:
                await interaction.response.send_message(f"{response['mensagem']} 🔵", ephemeral=True)
            else:
                await interaction.response.send_message(f"{interaction.user}, erro ao enviar a resposta. ❌", ephemeral=True)


    @app_commands.command(name="narrativo", description="Responder a um narrativo")
    async def responder_narrativo_command(self, interaction: discord.Interaction, gabarito: int):
        pergunta = await self.pegar_narrativo(gabarito)
        if pergunta:
            mymodal = self.MyModal(narrativo_instance=self, pergunta=pergunta, numero_gabarito=gabarito)
            await interaction.response.send_modal(mymodal)
        else:
            await interaction.response.send_message(f"{interaction.user}, não foi possível obter a pergunta do gabarito. 🔴", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Narrativo(bot))
