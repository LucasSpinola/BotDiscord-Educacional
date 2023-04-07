from discord.ext import commands
import settings
import discord

logger = settings.logging.getLogger('bot')


class WelcomeBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='Aluno')
        await member.add_roles(role)
        
async def setup(bot):
    welcome_bot = WelcomeBot(bot)
    await bot.add_cog(welcome_bot)