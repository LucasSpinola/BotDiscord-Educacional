import discord
from discord.ext import commands
import time
import os
import logging
import settings

logger = settings.logging.getLogger("bot")
                    
def run():
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
    
    async def carregar_cogs():
            for arquivo in os.listdir("cogs"):
                if arquivo.endswith(".py"):
                    await bot.load_extension(f"cogs.{arquivo[:-3]}")
    @bot.event
    async def on_ready():
        prfx = (time.strftime("%H:%M:%S UTC", time.gmtime()))
        logger.info(f"{prfx} 🤖 Bot iniciado com sucesso! {bot.user.name}")
        logger.info(f"{prfx} 🤖 ID do bot: {bot.user.id}")
        logger.info(f"{prfx} 🤖 Versão do Discord: {discord.__version__}")
        logger.info(f"{prfx} 🤖 Conectado em {len(bot.guilds)} servidores")
        
        await carregar_cogs()
        await bot.tree.sync()
        
        for cmd_file in os.listdir("cmds"):
            if cmd_file.endswith(".py") and not cmd_file.startswith("__"):
                await bot.load_extension(f"cmds.{cmd_file[:-3]}")
        
    bot.run(os.getenv('TOKEN'), root_logger=True)
    
if __name__ == '__main__':
    run()
