import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ...

    @commands.command()
    async def ola(self, ctx, *, member: discord.Member):
        await ctx.send("Olá {member.name} 👋!")
    
async def setup(bot):
    await bot.add_cog(Greetings(bot))