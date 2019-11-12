import discord
from discord.ext import commands
import asyncpg
import asyncio
from PIL import ImageDraw, Image, ImageFont
import aiohttp


class CrewSystem:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.pool.execute('CREATE TABLE IF NOT EXISTS user_crews('
                                    'id SERIAL NOT NULL PRIMARY KEY,'
                                    'name varchar(50) NOT NULL,'
                                    'captain bigint NOT NULL'
                                    'crew_members bigint[]'
                                    ')')



def setup(bot):
    bot.add_cog(CrewSystem(bot))
