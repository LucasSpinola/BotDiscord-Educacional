import discord
from discord.ext import commands
import requests
import os
from discord import app_commands

class Miniteste(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.pro.br:8000/api/v1/alunos/le_aluno"
        self.token = os.getenv('API_TOKEN')
        self.api_miniteste = "http://apibot.orivaldo.pro.br:8000/api/v1/miniteste/pegar/{teste}"
        self.api_miniteste_resposta = "http://apibot.orivaldo.pro.br:8000/api/v1/miniteste/adicionar/resposta"

    async def get_student_info(self, id: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_url}/{id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for aluno_id, aluno_data in data.items():
                if aluno_data['id_discord'] == id:
                    return aluno_data['turma'], aluno_data['matricula']
        return None, None, None

    async def add_resposta(self, matricula: int, teste: str, turma: str, resposta: str):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        data = {"matricula": matricula, "n_teste": teste, "sigla": turma, "resposta": resposta}
        response = requests.post(self.api_miniteste_resposta, json=data, headers=headers)
        if response.status_code == 200:
            return True

    @app_commands.command(name="miniteste", description="Teste de conhecimento!")
    async def miniteste(self, interaction: discord.Interaction, teste: str):
        try:
            teste_id = int(teste)
            aluno_id = str(interaction.user.id)
            turma, matricula = await self.get_student_info(aluno_id)
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(self.api_miniteste.format(teste=teste_id), headers=headers)

            if response.status_code == 200:
                data = response.json()
                pergunta = data["pergunta"]
                respostas = "\n".join(data["resposta"].values())
                n_teste = data["teste"]
                embed = discord.Embed(title=pergunta, description=respostas, color=0x0000FF)
                view = self.ButtonsFor(interaction, data["teste"], pergunta, respostas, turma, n_teste, matricula, self.add_resposta, self.bot)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.response.send_message(f"{interaction.user}, este teste não existe ou ocorreu um erro ao recuperar os dados. 🔴")
        except ValueError:
            await interaction.response.send_message(f"{interaction.user}, o número do teste deve ser um valor numérico. 🟡")

    class ButtonsFor(discord.ui.View):
        def __init__(self, interaction, nome, pergunta, respostas, n_teste, turma, matricula, add_resposta, bot):
            super().__init__(timeout=None)
            self.respondido = False
            self.nome_miniteste = nome
            self.pergunta = pergunta
            self.respostas = respostas
            self.interaction = interaction
            self.n_teste = n_teste
            self.turma = turma
            self.matricula = matricula
            self.add_resposta = add_resposta
            self.bot = bot

        @discord.ui.button(label="A", style=discord.ButtonStyle.blurple, custom_id="A")
        async def miniteste_A(self, interaction: discord.Interaction, button: discord.ui.Button):
            resposta = 'A'
            if not self.respondido:
                await interaction.response.send_message(f"{interaction.user}, sua respotas foi registrada! 🟢", ephemeral=True)
                await self.add_resposta(self.matricula, self.turma, self.n_teste, resposta)
                self.respondido = True
            else:
                await interaction.response.send_message(f"{interaction.user}, você já respondeu esse teste! 🔴", ephemeral=True)

        @discord.ui.button(label="B", style=discord.ButtonStyle.blurple, custom_id="B")
        async def miniteste_B(self, interaction: discord.Interaction, button: discord.ui.Button):
            resposta = 'B'
            if not self.respondido:
                await interaction.response.send_message(f"{interaction.user}, sua respotas foi registrada! 🟢", ephemeral=True)
                await self.add_resposta(self.matricula, self.turma, self.n_teste, resposta)
                self.respondido = True
            else:
                await interaction.response.send_message(f"{interaction.user}, você já respondeu esse teste! 🔴", ephemeral=True)

        @discord.ui.button(label="C", style=discord.ButtonStyle.blurple, custom_id="C")
        async def miniteste_C(self, interaction: discord.Interaction, button: discord.ui.Button):
            resposta = 'C'
            if not self.respondido:
                await interaction.response.send_message(f"{interaction.user}, sua respotas foi registrada! 🟢", ephemeral=True)
                await self.add_resposta(self.matricula, self.turma, self.n_teste, resposta)
                self.respondido = True
            else:
                await interaction.response.send_message(f"{interaction.user}, você já respondeu esse teste! 🔴", ephemeral=True)

        @discord.ui.button(label="D", style=discord.ButtonStyle.blurple, custom_id="D")
        async def miniteste_D(self, interaction: discord.Interaction, button: discord.ui.Button):
            resposta = 'D'
            if not self.respondido:
                await interaction.response.send_message(f"{interaction.user}, sua respotas foi registrada! 🟢", ephemeral=True)
                await self.add_resposta(self.matricula, self.turma, self.n_teste, resposta)
                self.respondido = True
            else:
                await interaction.response.send_message(f"{interaction.user}, você já respondeu esse teste! 🔴", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Miniteste(bot))