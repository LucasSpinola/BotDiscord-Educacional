import discord
from discord.ext import commands
from discord import app_commands

class Ajuda(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ajuda", description="Comandos do Bot!")
    async def ajuda(self, interaction: discord.Interaction):
        embedVar = discord.Embed(title="Ajuda", description="Lista de comandos disponíveis para alunos", color="0x0000FF")
        embedVar.add_field(name="/cadastrar {matricula}", value="Use esse comando para se cadastrar no banco de dados e poder registrar sua presença", inline=False)
        embedVar.add_field(name="/pergunta", value="Comando utilizado para fazer uma pergunta ao bot. Mensagens diretas ao bot também serão tratadas como perguntas, se não contiverem um comando específico", inline=False)
        embedVar.add_field(name="/presença", value="Use esse comando para registrar sua presença no dia", inline=False)
        embedVar.add_field(name="/miniteste {0-17}", value="Começa um miniteste", inline=False)
        embedVar.add_field(name="/verminitestes", value="Use para ver quais minitestes ja foram feitos", inline=False)
        embedVar.add_field(name="/redes", value="Este comando mostra as redes sociais do professor Orivaldo", inline=False)
        embedVar.add_field(name="/comandos", value="Mostra os comandos para monitores e professores", inline=False)
        await interaction.response.send_message(embed=embedVar)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))
