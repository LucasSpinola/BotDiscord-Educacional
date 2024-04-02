import discord
from discord.ext import commands
from discord import app_commands
import os
import requests

API = os.getenv('API_URL')

class Ajuda(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
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

    @app_commands.command(name="ajuda", description="Comandos do Bot!")
    async def ajuda(self, interaction: discord.Interaction):
        embedVar = discord.Embed(title="Ajuda", description="Lista de comandos disponíveis para alunos", color=0x0000FF)
        embedVar.add_field(name="/cadastrar {matricula}", value="Use esse comando para se cadastrar no banco de dados e poder registrar sua presença", inline=False)
        embedVar.add_field(name="/pergunta", value="Comando utilizado para fazer uma pergunta ao bot. Mensagens diretas ao bot também serão tratadas como perguntas, se não contiverem um comando específico", inline=False)
        embedVar.add_field(name="/presença", value="Use esse comando para registrar sua presença no dia", inline=False)
        embedVar.add_field(name="/miniteste {0-17}", value="Começa um miniteste", inline=False)
        embedVar.add_field(name="/narrativo {numero}", value="Escreva um algorimto em liguagem narrativa conforme pede a questão!", inline=False)
        embedVar.add_field(name="/verminitestes", value="Use para ver quais minitestes ja foram feitos", inline=False)
        embedVar.add_field(name="/redes", value="Este comando mostra as redes sociais do professor Orivaldo", inline=False)
        embedVar.add_field(name="/comandos", value="Mostra os comandos para monitores e professores", inline=False)
        await interaction.response.send_message(embed=embedVar)
        
    
    @app_commands.command(name="comandos", description="Comandos para monitores e professores")
    async def comandos(self, interaction: discord.Interaction):
        id_user = str(interaction.user.id)
        check_permission = await self.check_permission(id_user)
        if check_permission == True:
            embedVar = discord.Embed(title="Comandos para monitores e professores", description="Lista de comandos disponíveis para monitores e professores", color=0x0000FF)
            embedVar.add_field(name="/criaraluno {nome} {matricula} {turma} {subturma}", value="Cria um novo aluno no banco de dados", inline=False)
            embedVar.add_field(name="/buscaraluno {matricula}", value="Busca um aluno no banco de dados", inline=False)
            embedVar.add_field(name="/resetarid {matricula} {id_discord}", value="Reseta o ID do aluno no banco de dados", inline=False)
            embedVar.add_field(name="/darpermissao {id_discord} {nome} {cargo}", value="Dá permissão para um usuário", inline=False)
            embedVar.add_field(name="/darpresenca {matricula} {turma} {data}", value="Da presença a um aluno em uma determinada data informada. Use o formato YYYY-MM-DD", inline=False)
            embedVar.add_field(name="/userinfo", value="Mostra os dados de um aluno específico", inline=False)
            embedVar.add_field(name="/minhasturmas", value="Mostra as turmas que estão cadastradas no seu ID", inline=False)
            embedVar.add_field(name="/chamada {turma}", value="Veja a frequencia da sua turma hoje", inline=False)
            embedVar.add_field(name="/resultadoteste {turma} {teste}", value="Mostra os minitestes respondidos de uma determinada turma", inline=False)
            embedVar.add_field(name="/criarpergunta {pergunta} {resposta}", value="Cria uma pergunta no banco de dados", inline=False)
            embedVar.add_field(name="/criarnarrativo", value="Cria uma pergunta e resposta de um algoritmo de linguagem narrativa", inline=False)
            embedVar.add_field(name="/baixarfrquencia {turma}", value="Use para baixar a frequência da turma que foi selecionada.", inline=False)
            await interaction.response.send_message(embed=embedVar)
            
        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))
