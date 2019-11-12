import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(
            title='Here is a list of commands',
            description='__^-^-^-^-^-^-^-^-^-^-^-^-^-^__',
            color=0x00ffa9
        )
        help_embed.set_author(name=self.bot.user.name + ' - Help', icon_url=self.bot.user.avatar_url)
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        await about_command(help_embed)
        await role_command(help_embed)
        await char_commands(help_embed)
        await ranking_commands(help_embed)
        await ctx.send(embed=help_embed)


async def about_command(embed: discord.Embed):
    embed.add_field(name='__About__ - o!about', value='Get to know me ^-^\n__\n__')


async def role_command(embed: discord.Embed):
    embed.add_field(name='__Role__ - o!role', value='Trigger the command and react to the color of the '
                                                    'role you want to assign to yourself\nNote: You can change your '
                                                    'role once every 3 days, 2 hours\n__\n__', inline=False)


async def char_commands(embed: discord.Embed):
    embed.add_field(name='__Character Database__', value='**o!charlist <character_name>** - Get a list of variants of '
                                                         'a specific character\n    Ex: **o!charlist luffy**\n\n'
                                                         '**o!char <char_name>/<char_id>** - View the stats of a unit\n'
                                                         'ex: **o!char luffy** or **o!char 39**\n\n'
                                                         '**o!art <char_name>** - View the art of a unit\n'
                                                         'Ex: **o!art luffy**\n__\n__', inline=False)


async def ranking_commands(embed: discord.Embed):
    embed.add_field(name='__Pirate Ranks__', value="Ranking system based on member activity in the server. Member's bounty increases every level. A badge is acquired every 10 levels "
                                                   'Reaching level 100 assigns the member the Pirate King role (More rewards to be added soon). '
                                                   'Activity in the channels that have been blacklisted will not be taken into account.\n'
                                                   "**o!poster** - Display the member's wanted poster.\nReacting 🅱 shows a list of the member's badges *(this reaction will first be added by the bot"
                                                   "if the member has at least 1 badge)*\n"
                                                   "**o!bulletin** - Lists the top 10 most active members\n\n")


def setup(bot):
    bot.add_cog(Help(bot))
