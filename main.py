import settings
import discord
from discord.ext import commands
import requests
from discord import utils
from discord.ext.commands import Context
from cogs.greetings import Greetings
import pathlib
from re import A
import datetime
from api import get_aluno_id, get_nome, set_presenca
from colorama import Back, Fore, Style
import time
import asyncio


logger = settings.logging.getLogger('bot')


def run():
    intents = discord.Intents.all()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.command()
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def monitor(ctx):
        await ctx.send("Você é monitor! ✔️")
    
    
    
    
    @bot.event
    async def on_ready():
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        logger.info(prfx + " 🤖 Bot iniciado com sucesso! " + Fore.YELLOW + bot.user.name)
        logger.info(prfx + " 🤖 ID do bot: " + Fore.YELLOW + str(bot.user.id))
        logger.info(prfx + " 🤖 Versão do Discord: " + Fore.YELLOW + discord.__version__)
        await bot.tree.sync()
       
        #mygroup = MyGroup(name="Ajuda", description="Comando para ajuda")
        #bot.tree.add_command(mygroup)
        await bot.load_extension("slashcmds.bemvindo")
        await bot.load_extension("cogs.welcomebot")

    
    @bot.command()
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
    
    @bot.command()
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def unload(ctx, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}")
    
    @bot.command()
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
    
    
        
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você esqueceu de colocar um argumento! ❌")
          
    
    @bot.tree.context_menu(name="Ver data que entrou no servidor")
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def entrada_server(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"Usuário: ***{member}*** entrou no servidor em:{discord.utils.format_dt(member.joined_at)} 📅", ephemeral=True)
    
    @bot.tree.context_menu(name="Reportar Mensagem")
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Mensagem reportada ✅", ephemeral=True)
    
    @bot.tree.command(name="userinfo", description="Mostra informações do usuário.")
    async def userinfo(interaction: discord.Interaction, member:discord.Member=None):
        if member == None:
            member = interaction.user
        roles = [role for role in member.roles]
        embed = discord.Embed(title="Informações do usuário", description=f"Aqui estão as informações do usuário:", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nome:", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Nickname:", value=member.display_name)
        embed.add_field(name="Status:", value=member.status)
        embed.add_field(name="Criado em:", value=member.created_at.strftime("%a, %B %#d %Y, %I:%M %p "))
        embed.add_field(name="Entrou em:", value=member.joined_at.strftime("%a, %B %#d %Y, %I:%M %p "))
        embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top Role:", value=member.top_role.mention)
        embed.add_field(name="Bot:", value=member.bot)
        await interaction.response.send_message(embed=embed)
    
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def adm(ctx):
        await ctx.message.delete()
        # Código do comando exclusivo para Monitor aqui
        await ctx.author.send("Você é administrador do Bot! ✅")


    async def has_role(message: discord.Message, role_name: str) -> bool:
        """
        
        Args:
            message (discord.Message): A mensagem que foi enviada pelo usuário.
            role_name (str): O nome do cargo que deve ser verificado.
            
        Returns:
            bool: True se o usuário tem o cargo, False caso contrário.
        """
        guild = message.guild
        author = message.author
        role = discord.utils.get(guild.roles, name=role_name)
        
        if role is None:
            raise ValueError(f"O cargo {role_name} não existe neste servidor. ❌")
            
        return role in author.roles
    
    class Buttons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Fluxograma", style=discord.ButtonStyle.blurple, custom_id="1")
        async def miniteste1(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            await interaction.channel.send(content=f"{member.name} sua respotas está incorreta, tente novamente! 🔴")
    
        @discord.ui.button(label="Linguagem Narrativa", style=discord.ButtonStyle.blurple, custom_id="2")
        async def miniteste2(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            await interaction.channel.send(content=f"{member.name} sua respotas está incorreta, tente novamente! 🔴")
    
        @discord.ui.button(label="Pseudocódigo", style=discord.ButtonStyle.blurple, custom_id="3")
        async def miniteste3(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            await interaction.channel.send(content=f"{member.name} sua respotas está correta! 🟢")
        
        @discord.ui.button(label="Linguagem de Programação", style=discord.ButtonStyle.blurple, custom_id="4")
        async def miniteste4(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            await interaction.channel.send(content=f"{member.name} sua respotas está incorreta, tente novamente! 🔴")
            
    
    @bot.tree.command(name="miniteste", description="Teste de conhecimento!")
    async def miniteste(interaction: discord.Interaction):
        await interaction.response.send_message(content="Qual a forma mais imprecisa de representação de algoritmos?", view=Buttons())
    
    class ButtonsTwo(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Youtube", style=discord.ButtonStyle.red, custom_id="5")
        async def redes1(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.channel.send(content="Canal do professor: https://www.youtube.com/@orivaldo 🟥")
        
        @discord.ui.button(label="Email", style=discord.ButtonStyle.blurple, custom_id="6")
        async def redes2(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.channel.send(content="Email do professor: orivaldo@gmail.com 📨")
        
        @discord.ui.button(label="Github", style=discord.ButtonStyle.green, custom_id="7")
        async def redes3(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.channel.send(content="Github do professor: https://github.com/orivaldosantana/ECT2203LoP 🐱‍👤")
        
    @bot.tree.command(name="redes", description="Redes sociais do professor!")
    async def redes(interaction: discord.Interaction):
        await interaction.response.send_message(content="Aqui estão as redes sociais do professor!", view=ButtonsTwo())
    
    
    
    @bot.command()
    async def pergunta(ctx, *, input_mensagem=''):
        input_mensagem = ctx.message.content
        input_mensagem = input_mensagem.replace("!pergunta", '')

        r = requests.post('http://apibot.orivaldo.net:8000/pergunta', json={
        "mensagem": input_mensagem
    })
        await ctx.send(f"Olá ***{ctx.author.name}*** achamos essa resposta para você,\n{r.json()}")
        #await ctx.send(f"{r.json()}")
    
    
    @bot.command()
    async def presenca(ctx, matricula =""):
        
        matricula = ctx.message.content
        matricula = matricula.replace("!presenca ", '')
        
        aluno_id = get_aluno_id(matricula)

        data = datetime.datetime.now()
        #data = data.strftime("%d-%x-%y")


        set_presenca(str(data)[0:10:1], aluno_id)

        nome = get_nome(matricula)

        await ctx.send(f"✅​ {nome}, sua presença foi registrada com sucesso!")
        
    @bot.event
    @commands.check(lambda ctx: has_role(ctx.message, "BOT-ADM"))
    async def dataprova(message):    
            data_hora = message.content[11:]
            data_hora_obj = datetime.datetime.strptime(data_hora, '%d/%m/%Y %H:%M')
            agora = datetime.datetime.now()
            await message.delete()
            if data_hora_obj < agora:
                await message.author.send('Desculpe, não posso criar um lembrete para o passado. ⏰')
                return
            else:
                await message.author.send(f'Data cadastrada com sucesso! "***{message.content[11:]}***" ⌛')

            diferenca = (data_hora_obj - agora).total_seconds()
            await asyncio.sleep(diferenca)
            await message.channel.send(f'Hoje teremos ***Prova***, não esqueça de olhar o Sigaa! 📝')
        
    bot.run(settings.TOKEN_BOT, root_logger=True)

if __name__ == '__main__':
    run()