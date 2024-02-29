import discord
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import os

class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = "http://apibot.orivaldo.net:8000/api/v1/alunos/le_aluno"
        self.token = os.getenv('API_TOKEN')
        self.api_permissao = "http://apibot.orivaldo.net:8000/api/v1/permissao/verificar"
        self.api_autorizado = "http://apibot.orivaldo.net:8000/api/v1/permissao/pegar_permissao"

    async def get_student_info(self, id: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_url}/{id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    async def process_student_data(self, api_data, discord_id: str):
        if api_data is None:
            return "Não cadastrado", "Não cadastrado", "Não cadastrado", "Não cadastrado"
        
        for aluno_id, aluno_data in api_data.items():
            if aluno_data['id_discord'] == discord_id:
                nome = aluno_data['nome'] if aluno_data['nome'] else "Não cadastrado"
                matricula = aluno_data['matricula'] if aluno_data['matricula'] else "Não cadastrado"
                turma = aluno_data['turma'] if aluno_data['turma'] else "Não cadastrado"
                sub_turma = aluno_data['sub_turma'] if aluno_data['sub_turma'] else "Não cadastrado"
                return nome, matricula, turma, sub_turma
        else:
            return "Não cadastrado", "Não cadastrado", "Não cadastrado", "Não cadastrado"

    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}?id_discord={id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'permissao' in data and data['permissao'].lower() == id_discord.lower():
                return True
            else:
                return False

    async def get_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_autorizado}?id_discord={id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None


    @app_commands.command(name="userinfo", description="Mostra informações do usuário.")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        id_user = str(interaction.user.id)
        if member is None:
            member = interaction.user

        check_permission = await self.check_permission(id_user)
        if check_permission == True:

            student_data = await self.get_student_info(str(member.id))
            nome, matricula, turma, sub_turma = await self.process_student_data(student_data, str(member.id))
            embed = discord.Embed(title="📄 Informações do usuário:", color=0x0000FF, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name="🆔 ID:", value=member.id)
            embed.add_field(name="👤 Nome:", value=nome)
            embed.add_field(name="🎓 Matrícula:", value=matricula)
            embed.add_field(name="🏷️ Nick:", value=f"{member.name}#{member.discriminator}")
            embed.add_field(name="🗂️ Turma:", value=turma)
            embed.add_field(name="📚 Sub-Turma:", value=sub_turma)
            embed.add_field(name="📅 Criado em:", value=member.created_at.strftime("%#d %B %Y "))
            embed.add_field(name="🚪 Entrou em:", value=member.joined_at.strftime("%a, %#d %B %Y "))
            embed.add_field(name=f"💼 Cargos ({len(member.roles)})", value=" ".join([role.mention for role in member.roles]))
            embed.add_field(name="🤖 Bot:", value=member.bot)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        else:
            await interaction.response.send_message(f"{member.name}, você não tem permissão para usar este comando. ❌", ephemeral=True)

    
    @app_commands.command(name="myuser", description="Mostra informações do seu perfil no servidor.")
    async def myuser(self, interaction: discord.Interaction):
        member = interaction.user
        student_data = await self.get_student_info(member.id)
        nome, matricula, turma, sub_turma = await self.process_student_data(student_data, str(member.id))
        embed = discord.Embed(title="📄 Informações do seu usuário:", color=0x0000FF, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="🆔 ID:", value=member.id)
        embed.add_field(name="👤 Nome:", value=nome)
        embed.add_field(name="🎓 Matrícula:", value=matricula)
        embed.add_field(name="🏷️ Nick:", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="🗂️ Turma:", value=turma)
        embed.add_field(name="📚 Sub-Turma:", value=sub_turma)
        embed.add_field(name="🤖 Bot:", value=member.bot)
        embed.add_field(name="📅 Criado em:", value=member.created_at.strftime("%#d %B %Y "))
        embed.add_field(name="🚪 Entrou em:", value=member.joined_at.strftime("%a, %#d %B %Y "))
        embed
        await interaction.response.send_message(embed=embed, ephemeral=True)
    

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
