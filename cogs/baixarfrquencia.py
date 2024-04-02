import discord
from discord.ext import commands
import requests
from discord import app_commands
import os
import xlsxwriter
import io

API = os.getenv('API_URL')

class Baixafreq(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_freq = "{API}/api/v1/presenca/pegar_frequencias"
        self.api_data = "{API}/api/v1/unidades/lista_unidade"
        self.api_permissao = "{API}/api/v1/permissao/pegar_permissao"
        self.token = os.getenv('API_TOKEN')

    async def pegar_frequencia(self, turma: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_freq}/{turma}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('frequencias', {})
        return {}

    async def get_datas_unidades(self, turma: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_data}/{turma}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('unidades', {})
        return {}
    
    async def check_permission(self, id_discord: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.api_permissao}/{id_discord}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            api_id_discord = data.get('id', '')
            if api_id_discord == id_discord:
                return True
        return False

    @app_commands.command(name="baixarfrequencia", description="Baixe a frequência de uma turma")
    async def baixarfreq(self, interaction: discord.Interaction, turma: str):
        id_user = str(interaction.user.id)
        check_permission = await self.check_permission(id_user)
        if check_permission == True:
            unidade = await self.get_datas_unidades(turma)
            freq = await self.pegar_frequencia(turma)

            
            dias = []
            for matricula, info in freq.items():
                for dia, presenca in info.get('frequencia', {}).items():
                    if dia not in dias:
                        dias.append(dia)
                    if isinstance(presenca, list):
                        for p in presenca:
                            if f"{dia}-{p}" not in dias:
                                dias.append(f"{dia}-{p}")
            
            dias = sorted(dias)

            excel_buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(excel_buffer, {'in_memory': True})
            pag = workbook.add_worksheet(name='frequências')

            pag.write(0, 0, "Aluno")

            for i, dia in enumerate(dias):
                pag.write(0, i+1, dia)

            posicao = 1
            for matricula, info in freq.items():
                matriculas = info.get('matricula', {})
                matriculas_sem_virgula = str(matriculas).replace(",", "")
                pag.write(posicao, 0, matriculas_sem_virgula)
                for i, dia in enumerate(dias):
                    presenca = info.get('frequencia', {}).get(dia)
                    if presenca is None:
                        pag.write(posicao, i+1, 0)
                    else:
                        if isinstance(presenca, list):
                            if any("A" in p for p in presenca):
                                pag.write(posicao, i+1, 0)
                            else:
                                pag.write(posicao, i+1, 1)
                        else:
                            pag.write(posicao, i+1, 1)
                posicao += 1

            workbook.close()
            excel_buffer.seek(0)

            await interaction.response.send_message(f'✅ {interaction.user}, arquivo xlsx gerado com sucesso.', file=discord.File(excel_buffer, filename=f'presenca_{turma}.xlsx'))

        else:
            await interaction.response.send_message(f"{interaction.user}, você não tem permissão para usar este comando. ❌", ephemeral=True)
async def setup(bot):
    await bot.add_cog(Baixafreq(bot))
