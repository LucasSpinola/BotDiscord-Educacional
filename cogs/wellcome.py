import discord
from discord.ext import commands

class Wellcome(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_remove(member: discord.Member):
        guild = member.guild
        canal = discord.utils.get(guild.channels,id=603318662228607018)
        embed = discord.Embed(title=f'Até logo {member.name}#{member.discriminator}, deixou o servidor.', color=0x0000FF)
        embed.set_author(name=member.name, icon_url=member.avatar)
        await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(member: discord.Member):
        guild = member.guild
        canal = discord.utils.get(guild.channels,id=603318662228607018)
        embed = discord.Embed(title=f'Olá {member.name} seja bem-vindo(a) ao servidor de LOP! \nQualquer dúvida use /ajuda \nLembre-se de respeitar as regras do servidor, promovendo um ambiente amigável e construtivo para todos.', color=0x0000FF)
        embed.set_author(name=member.name, icon_url=member.avatar)
        await canal.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Wellcome(bot))