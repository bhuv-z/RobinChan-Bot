import discord
from discord.ext import commands
import asyncio
import os
import sys
import datetime
import asyncpg
import json


with open("CREDENTIALS") as creds:
    creds = json.loads(creds.read())
    TOKEN = creds["TOKEN"]  
    credentials = {"user": creds["user"], "password": creds["password"], "database": creds["database"], "host": creds["host"]} # local host "127.0.0.1"
    
ver = json.loads(open("VERSION").read())["BOT_VERSION"]

class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(command_prefix="o!", case_insensitive=True)
        self.pool = None

    async def setup(self):
        self.pool = await asyncpg.create_pool(**credentials)


bot = Bot()

# -------------------- Loading Cogs(extensions) ------------------------------------#
bot.remove_command('help')  # remove default help command
if __name__ == '__main__':
    for extension in json.loads(open("cogs\\__ACTIVE_EXTENSIONS__").read()):
        try:
            bot.load_extension(extension)
            print(f'Cog: {extension} has been loaded')
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)

# ----------------------------------------------------------------------------------#


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(f'Created by Blaz#9195')


@bot.command()
@commands.is_owner()
async def reload(ctx, *, arg):
    """Reloads a module."""
    try:
        bot.unload_extension(arg)
        bot.load_extension(arg)
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send('Cog: `%s` reloaded successfully' % arg)


# test
@bot.command()
@commands.is_owner()
async def test(ctx, *, arg):
    await ctx.send(arg + " <-- this means the bot is online.. nya >.<")


# About Command
@bot.command()
async def about(ctx):
    aboutEmbed = discord.Embed(
        title="A discord.py bot for One Piece Bounty Rush Discord Server",
        description="Type ``%s`` for a list of available commands\n__\n__" % "o!help",
        color=0x00ffd8
    )
    aboutEmbed.set_author(name=bot.user.name + ' - About', icon_url=bot.user.avatar_url)
    aboutEmbed.set_thumbnail(url=bot.user.avatar_url)
    aboutEmbed.add_field(name="Written By", value=(await bot.application_info()).owner.mention)
    aboutEmbed.add_field(name="Version", value=ver, inline=False)
    aboutEmbed.add_field(name="Git Repository", value="---")
    aboutEmbed.add_field(name="Contributor(s)", value=f"{bot.get_user(119149398306455552).mention} - Data Collection")
    await ctx.send(embed=aboutEmbed)


@bot.command()
@commands.is_owner()
async def terminate(ctx):
    await ctx.send('**Terminating Bot**\n\n*bye bye*\nT~T')
    await bot.pool.close()
    await bot.logout()

bot.loop.create_task(bot.setup())
bot.run(TOKEN)

#-------- Zephyr毒ivy was here O<-<
