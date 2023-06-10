import settings
import discord
from discord.ext import commands
import requests
from discord import utils, app_commands, ui
from discord.ext.commands import Context
import pathlib
from re import A
import datetime
from api import get_aluno_id, get_nome, set_presenca, comparar_id, add_id, get_id, reset_id, get_turma, add_resposta, cria_aluno, cria_pergunta, le_logs, deleta_logs, get_log
from colorama import Back, Fore, Style
import time
import asyncio
import os
import json


logger = settings.logging.getLogger('bot')

def run():
    
    intents = discord.Intents.all()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
    
    @bot.event
    async def on_ready():
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        logger.info(prfx + " 🤖 Bot iniciado com sucesso! " + Fore.YELLOW + bot.user.name)
        logger.info(prfx + " 🤖 ID do bot: " + Fore.YELLOW + str(bot.user.id))
        logger.info(prfx + " 🤖 Versão do Discord: " + Fore.YELLOW + discord.__version__)
        await bot.tree.sync()

    
    # funçaõ para caso der erro.    
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você esqueceu de colocar um argumento! ❌")
          
    
    #Puxa as informações dos alunos.
    @bot.tree.command(name="userinfo", description="Mostra informações do usuário.")
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def info(interaction: discord.Interaction, member:discord.Member=None):
        if member == None:
            member = interaction.user
        roles = [role for role in member.roles]
        id = value=member.id
        matricula = get_id(id)
        nome = get_nome(matricula)
        turma = get_turma(matricula)
        embed = discord.Embed(title="Informações do usuário", description=f"Aqui estão as informações desse usuário.", color=0x0000FF, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nome:", value=nome)
        embed.add_field(name="Matrícula:", value=matricula)
        embed.add_field(name="Nick:", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Turma:", value=turma)
        embed.add_field(name="Criado em:", value=member.created_at.strftime("%#d %B %Y "))
        embed.add_field(name="Entrou em:", value=member.joined_at.strftime("%a, %#d %B %Y "))
        #embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Status:", value=member.status)
        embed.add_field(name="Bot:", value=member.bot)
        
        await interaction.response.send_message(embed=embed)
    
    #Comando para ver se possuí o cargo ADM Técnico.
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico"))
    async def adm(ctx):
        await ctx.message.delete()
        # Código do comando exclusivo para Monitor aqui
        await ctx.author.send("Você é administrador do Bot! ✅")


    async def has_role(message: discord.Message, role_name: str) -> bool:

        guild = message.guild
        author = message.author
        role = discord.utils.get(guild.roles, name=role_name)
        
        if role is None:
            raise ValueError(f"O cargo {role_name} não existe neste servidor. ❌")
            
        return role in author.roles
    
    #Comando para ver se possuí o cargo MONITOR.
    @commands.check(lambda ctx: has_role(ctx.message, "MONITOR"))
    async def monitor(ctx):
        await ctx.message.delete()
        # Código do comando exclusivo para Monitor aqui
        await ctx.author.send("Você é monitor do Bot! ✅")


    async def has_role(message: discord.Message, role_name: str) -> bool:

        guild = message.guild
        author = message.author
        role = discord.utils.get(guild.roles, name=role_name)
        
        if role is None:
            raise ValueError(f"O cargo {role_name} não existe neste servidor. ❌")
            
        return role in author.roles
    
    # classe para mostrar os botões do miniteste1.
    class Buttons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.respondido = False
        @discord.ui.button(label="Fluxograma", style=discord.ButtonStyle.blurple, custom_id="1")
        async def miniteste1(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T1', 'A')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="Linguagem Narrativa", style=discord.ButtonStyle.blurple, custom_id="2")
        async def miniteste2(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T1', 'B')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="Pseudocódigo", style=discord.ButtonStyle.blurple, custom_id="3")
        async def miniteste3(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T1', 'C')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
        
        @discord.ui.button(label="Linguagem de Programação", style=discord.ButtonStyle.blurple, custom_id="4")
        async def miniteste4(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T1', 'D')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
    # função que chama a classe e apresenta o miniteste1.
    @bot.tree.command(name="miniteste", description="Teste de conhecimento!")
    async def miniteste(interaction: discord.Interaction):
        embed = discord.Embed(title="Qual a forma mais imprecisa de representação de algoritmos?", color=0x0000FF)
        await interaction.response.send_message(embed=embed, view=Buttons())
    
    
    # classe para mostrar os botões do miniteste2.    
    class ButtonsTree(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.respondido = False
        @discord.ui.button(label="A", style=discord.ButtonStyle.blurple, custom_id="5")
        async def miniteste5(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T2', 'A')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="B", style=discord.ButtonStyle.blurple, custom_id="6")
        async def miniteste6(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T2', 'B')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="C", style=discord.ButtonStyle.blurple, custom_id="7")
        async def miniteste7(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T2', 'C')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
        
        @discord.ui.button(label="D", style=discord.ButtonStyle.blurple, custom_id="8")
        async def miniteste8(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T2', 'D')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
    # função que chama a classe e apresenta o miniteste2.
    @bot.tree.command(name="miniteste2", description="Teste de conhecimento 2!")
    async def miniteste2(interaction: discord.Interaction):
        embed2 = discord.Embed(title="Qual das sequências de passos abaixo mais se assemelha a um algoritmos para calcular a média de dois números A e B.", description=f"a) Mostrar o Resultado;  Dividir por 2; Ler Número A e Número B; Somar A e B;\nb) Ler Número A e Número B; Somar A e B; Dividir por 2; Mostrar o Resultado;\nc) Dividir por 2; Mostrar o Resultado;  Ler Número A e Número B; Somar A e B;\nd) Ler Número A e Número B; Dividir por 2; Mostrar o Resultado;  Somar A e B;", color=0x0000FF)
        await interaction.response.send_message(embed=embed2, view=ButtonsTree())
    
    # classe para mostrar os botões do miniteste3.   
    class ButtonsFor(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.respondido = False
        @discord.ui.button(label="A", style=discord.ButtonStyle.blurple, custom_id="9")
        async def miniteste9(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T3', 'A')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="B", style=discord.ButtonStyle.blurple, custom_id="10")
        async def miniteste10(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T3', 'B')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="C", style=discord.ButtonStyle.blurple, custom_id="11")
        async def miniteste11(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T3', 'C')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
        
        @discord.ui.button(label="D", style=discord.ButtonStyle.blurple, custom_id="12")
        async def miniteste12(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = value=member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, 'T3', 'D')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
    # função que chama a classe e apresenta o miniteste3.
    @bot.tree.command(name="miniteste3", description="Teste de conhecimento 3!")
    async def miniteste3(interaction: discord.Interaction):
        embed3 = discord.Embed(title="O que é uma variável, no contexto de uma linguagem de programação?", description=f"a) Uma função.\nb) Um contador.\nc) Uma pessoa que varia (inconstante).\nd) Um espaço de memória para armazenar um determinado tipo de dado.", color=0x0000FF)
        await interaction.response.send_message(embed=embed3, view=ButtonsFor())
    
    
    # classe para mostrar os botões das redes sociais.   
    class ButtonsTwo(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Youtube", style=discord.ButtonStyle.red, custom_id="5")
        async def redes1(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.send_message(content="Canal do professor: https://www.youtube.com/@orivaldo 🟥")
        
        @discord.ui.button(label="Email", style=discord.ButtonStyle.blurple, custom_id="6")
        async def redes2(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.send_message(content="Email do professor: orivaldo@gmail.com 📨")
        
        @discord.ui.button(label="Github", style=discord.ButtonStyle.green, custom_id="7")
        async def redes3(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.send_message(content="Github do professor: https://github.com/orivaldosantana/ECT2203LoP 🐱‍👤")
    
    # função que chama a classe e apresenta a redes sociais do professor.    
    @bot.tree.command(name="redes", description="Redes sociais do professor!")
    async def redes(interaction: discord.Interaction):
        embed4 = discord.Embed(title="Aqui estão as redes sociais do professor Orivaldo!", color=0x0000FF)
        await interaction.response.send_message(embed=embed4, view=ButtonsTwo())

    
    # função pergunta.
    @bot.command()
    async def pergunta(ctx, *, input_mensagem=''):
        input_mensagem = ctx.message.content
        input_mensagem = input_mensagem.replace("!pergunta", '')

        r = requests.post('apibot.orivaldo.net:8000/pergunta', json={
        "mensagem": input_mensagem
    })
        await ctx.send(f"Olá ***{ctx.author.name}*** achamos essa resposta para você,\n{r.json()}")
    
    # função para cadastrar o id do discord ao usuário no banco de dados. ex: !cadastrar matricula
    @bot.command()
    async def cadastrar(ctx, matricula =""):
        id = str(ctx.author.id)
        matricula = ctx.message.content
        matricula = matricula.replace("!cadastrar ", '')
        aluno_id = get_aluno_id(matricula)
        validar = comparar_id(matricula)
        nome = get_nome(matricula)
        if validar == 0 or validar == None or validar == "0":
            add_id(aluno_id, id)
            await ctx.send(f"✅​ {nome}, seu id foi registrada com sucesso!")
        else:
            await ctx.send(f"❌​ {ctx.author.name}, você não tem permissão para registrar o id desse usuário!")
    
    # função que cadastra a presença do aluno ao banco de dados.
    @bot.command(aliases=['presença'])
    async def presenca(ctx):
        id = str(ctx.author.id)
        matricula = get_id(id)
        validar = comparar_id(matricula)
        aluno_id = get_aluno_id(matricula)
        nome = get_nome(matricula)
        if validar == id:
            data = datetime.datetime.now()
            #data = data.strftime("%d-%x-%y")
            set_presenca(str(data)[0:10:1], aluno_id)
            await ctx.send(f"✅​ {nome}, sua presença foi registrada com sucesso!")
        else:
            await ctx.send(f"❌​ {ctx.author.name}, você não tem permissão para registrar a presença desse usuário!")
    
    # função que reseta o id do usuário no banco de dados. ex: !resetarid matricula
    @bot.command()
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def resetarid(ctx, matricula =""):
        matricula = ctx.message.content
        matricula = matricula.replace("!resetarid ", '')
        aluno_id = get_aluno_id(matricula)
        if matricula != None:
            reset_id(aluno_id)
            await ctx.send(f"✅​ {ctx.author.name}, o id do usuário foi resetado com sucesso!")
        else:
            await ctx.send(f"❌​ {ctx.author.name}, você não tem permissão para resetar o id desse usuário!")
    
    # função para mostrar os comandos de ajuda.     
    @bot.command()
    async def ajuda(ctx):
        embedVar = discord.Embed(title="Comandos", description="Lista de comandos disponíveis para alunos e professores", color=0x00ff00)
        embedVar.add_field(name="!pergunta", value="o comando utlizado para perguntar algo ao bot, lembrando que mensagens diretas ao bot serão tratadas como perguntas diretamente se não elas não contém um comando específico", inline=False)
        embedVar.add_field(name="!presenca", value="use esse comando para registrar sua presença no dia", inline=False)
        embedVar.add_field(name="/miniteste", value="Começa um miniteste", inline=False)
        embedVar.add_field(name="/redes", value="o comando mostra a redes sociais do professor Orivaldo", inline=False)
        embedVar.add_field(name="!comandos", value="mostra os comandos para monitores e professores", inline=False)
        await ctx.message.author.send(embed=embedVar)    
    
    # função para mostrar os comandos dos monitores e professores.
    @bot.command()
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def comandos(ctx):
        embedVar = discord.Embed(title="Comandos", description="Lista de comandos disponíveis para alunos e professores", color=0x0000FF)
        embedVar.add_field(name="!pergunta", value="o comando utlizado para perguntar algo ao bot, lembrando que mensagens diretas ao bot serão tratads como perguntas diretamente se não elas não contém um comando específico", inline=False)
        embedVar.add_field(name="!cadastrar {matricula}", value="use esse comando para cadastrar seu id no banco de dados", inline=False)
        embedVar.add_field(name="!resetarid {matricula}", value="use esse comando para resetar o id no banco de dados", inline=False)
        embedVar.add_field(name="!presenca", value="use esse comando para registrar sua presença no dia", inline=False)
        embedVar.add_field(name="dataprova DD/MM/AAAA HH:MM", value="Manda um aviso do dia que será a prova", inline=False)
        embedVar.add_field(name="/criaraluno", value="o comando cria um aluno no banco de dados", inline=False)
        embedVar.add_field(name="/criapergunta", value="o comando cria uma pergunta e resposta no banco de dados", inline=False)
        embedVar.add_field(name="/responderlog", value="o comando responde um log armazenado no banco de dados e cria uma pergunta e resposta", inline=False)
        embedVar.add_field(name="/puxarlog", value="o comando puxa os log armazenado no banco de dados e cria uma pergunta e resposta", inline=False)
        embedVar.add_field(name="/miniteste", value="Começa um teste sobre Algoritimos", inline=False)
        embedVar.add_field(name="/userinfo", value="o comando mostra informações de determinado membro do servidor", inline=False)
        embedVar.add_field(name="/redes", value="o comando mostra a redes sociais do professor Orivaldo", inline=False)
        await ctx.message.author.send(embed=embedVar)    
    
    
    # função que marca a data da prova e no dia exato envia uma mensagem no canal avisando.
    @bot.event
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
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
    
    
    # classe de modal para criar um aluno.
    class MyModal(discord.ui.Modal, title="Criar Aluno"):
        nome = discord.ui.TextInput(label="Nome", placeholder="Digite o nome completo do aluno", min_length=1, max_length=100)
        matricula = discord.ui.TextInput(label="Matricula", placeholder="Digite a matrícula do aluno", min_length=1, max_length=100)
        turma = discord.ui.TextInput(label="Turma", placeholder="Digite a turma do aluno", min_length=1, max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            nome = self.nome.value
            matricula = self.matricula.value
            turma = self.turma.value
            cria_aluno(nome, matricula, turma, 0)
            await interaction.response.send_message(f"Aluno {nome} criado com sucesso! ✅​", ephemeral=True)
    
    # função que chama a classe e mostra o modal para criar o aluno no banco de dados.    
    @bot.tree.command(description="Cria um aluno no banco de dados")
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def criaraluno(interection: discord.Interaction):
        mymodal = MyModal()
        await interection.response.send_modal(mymodal)    
    
    # classe de modal para criar pergunta.
    class MyModalP(discord.ui.Modal, title="Criar Pergunta"):
        pergunta = discord.ui.TextInput(label="Pergunta", placeholder="Digite a pergunta", min_length=1, max_length=100)
        resposta = discord.ui.TextInput(label="Resposta", placeholder="Digite a resposta", min_length=1, max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            perguntas = self.pergunta.value
            respostas = self.resposta.value
            cria_pergunta(perguntas, respostas)
            await interaction.response.send_message(f"Pergunta <{perguntas}> criada com sucesso! ✅​", ephemeral=True)
    
     # função que chama a classe e mostra o modal para criar pergunta no banco de dados.      
    @bot.tree.command(description="Cria uma pergunta e resposta no banco de dados")
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def criarpergunta(interection: discord.Interaction):
        mymodal = MyModalP()
        await interection.response.send_modal(mymodal)
    
    # função para puxar os logs de perguntas sem respostas na API.
    @bot.tree.command(description="puxar os logs do banco de dados")
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def puxarlogs(interection: discord.Interaction):
        log = le_logs().json()
        logs_json = json.dumps(log, indent=4)
        
        await interection.response.send_message(logs_json)
    
    # classe para responder o log em aberto.
    class MyModalLogs(discord.ui.Modal, title="Responder Logs"):
        pergunta = discord.ui.TextInput(label="Pergunta", placeholder="Digite a pergunta", min_length=1, max_length=100)
        resposta = discord.ui.TextInput(label="Resposta", placeholder="Digite a resposta", min_length=1, max_length=100)
        log_pergunta = discord.ui.TextInput(label="Pergunta do log", placeholder="Digite o id do log", min_length=1, max_length=100)
        log_id = discord.ui.TextInput(label="Id do log (obs: -id)", placeholder="Digite o id do log", min_length=1, max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            perguntas = self.pergunta.value
            respostas = self.resposta.value
            logs_p = self.log_pergunta.value
            logs_id = self.log_id.value

            id_logs = get_log(logs_p)
            if id_logs == logs_id:
                deleta_logs(logs_id)
                cria_pergunta(perguntas, respostas)
                await interaction.response.send_message(f"Log <{logs_id}> respondido com sucesso! ✅​", ephemeral=True)
            else: 
                await interaction.response.send_message(f"Log <{logs_id}> não encontrado! ❌​", ephemeral=True)
    
    # função que chama a classe e mostra o modal para responder os logs no banco de dados.      
    @bot.tree.command(description="responde os logs do bot")
    @commands.check(lambda ctx: has_role(ctx.message, "ADM Técnico") and has_role(ctx.message, "MONITOR") and has_role(ctx.message, "PROFESSOR"))
    async def responderlog(interection: discord.Interaction):
        myModalLog = MyModalLogs()
        await interection.response.send_modal(myModalLog)
    
    
    
    bot.run(settings.TOKEN_BOT, root_logger=True)

if __name__ == '__main__':
    run()
