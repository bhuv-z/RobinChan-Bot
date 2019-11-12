"""UNDER WORKS"""

import discord
from discord.ext import commands
import asyncpg
import traceback
import asyncio
import aiohttp
import json
import os
from datetime import datetime, timedelta
import numpy as np

date = datetime.now()


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.recent_tournament_data = None
        # if os.path.exists('tournament_info.json'):
        #     with open('tournament_info.json', encoding='utf-8') as tourny:
        #         self.recent_tournament_data = json.loads(tourny.read())
        #         print('Loaded tournament_info.jso')

    @commands.Cog.listener()
    async def on_ready(self):
        if os.path.exists('tournament_info.json'):
            with open('tournament_info.json', encoding='utf-8') as tourny:
                self.recent_tournament_data = json.loads(tourny.read())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not self.bot.get_user(payload.user_id).bot:
            if str(payload.emoji) == self.recent_tournament_data["emoji"] and payload.message_id == self.recent_tournament_data["msg_id"]:

                # await self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id).send('pong')
                tourney_id = f'tournament_{self.recent_tournament_data["id"]}'
                user_id = payload.user_id

                # check if member already registered in the DB
                get_record = await self.bot.pool.fetch(f'SELECT ign from {tourney_id} WHERE user_id={user_id}')
                if get_record:
                    return
                # End initial Check

                pow_req = await self.bot.get_user(user_id).send("**Enter your maximum power level:** ex:``25000``")

                def check_1(m):
                    if m.channel == pow_req.channel and m.author.id == user_id:
                        return True

                pow_resp = await self.bot.wait_for('message', check=check_1)

                sup_req = await self.bot.get_user(user_id).send("**Enter you the Support Percentage of your team with the maximum power level:  ex: 27.4** *(Without the %)*")

                def check_2(m):
                    if m.channel == sup_req.channel and m.author.id == user_id:
                        return True

                sup_resp = await self.bot.wait_for('message', check=check_2)

                ign_req = await self.bot.get_user(user_id).send("**Enter your ingame name:**")

                def check_3(m):
                    if m.channel == ign_req.channel and m.author.id == user_id:
                        return True

                ign_resp = await self.bot.wait_for('message', check=check_3)

                rules_msg = await self.bot.get_user(user_id).send(
                                                        "__**Here are the rules to be followed till the tournament:**__\n"
                                                        "1. Do not change your ingame name\n"
                                                        "2. Let us know if there is a drastic change in your power level before the day of the tournament\n"
                                                        "\nIf you are unable to make it to the tournament, let an Admiral know in advance.\n"
                                                        "\n*As this system is just starting to be used to organize the tournament, you will be notified if problems arise and we are unable to hose the tournament*\n\n"
                                                        "React 👍 to this message to accept the terms listed above."
                                                        )
                await rules_msg.add_reaction('👍')

                def check_4(reaction, user):
                    if reaction.message.id == rules_msg.id and str(reaction.emoji) == '👍' and user.id == payload.user_id:
                        return True

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=180, check=check_4)

                    await self.bot.pool.execute(f'INSERT INTO {tourney_id} (user_id, ign, pow_lvl, sup_prct)'
                                                f'VALUES'
                                                f"({user_id}, '{ign_resp.content}', {pow_resp.content}, {sup_resp.content})")

                    await self.bot.get_user(user_id).send("You have successfully signed up for the tournament. Good Luck!")

                except TimeoutError:
                    await self.bot.get_user(user_id).send('The signup has timed out! You have not been added to the tournament roster.')

    # Start tournament - create tournament post and table and stuff
    @commands.command()
    @commands.is_owner()
    async def initiate_tournament(self, ctx):
        if self.recent_tournament_data:
            tourny_id = self.recent_tournament_data["id"] + 1
        else:
            tourny_id = 1

        tourny_announce = discord.Embed(
            title='One Piece Bounty Rush Tournament',
            description=f"A serverwide OPBR tournament is going to be held on ##DATE##\n",
            color=discord.Color.dark_orange(),
            timestamp=datetime.today()
        )
        tourny_announce.add_field(
            name='How to sign up?',
            value='*if you have "Allow direct messages from server members" turned disabled in this server, enable it before proceeding.*\n\n'
                  '1. React 🛡 to this message to signup for the tournament\n'
                  '2. Answer the questions prompted by the bot in your dms\n'
                  '\nIf you decide to unregister from the tournament, you can do so by using the command ``o!leavetournament`` in #bots\n\n'
        )
        msg = await ctx.guild.get_channel(596405900747735050).send(embed=tourny_announce)
        with open('tournament_info.json', 'w+', encoding='utf-8') as fout:
            out_str = '{' \
                      f'\t"id":{tourny_id},\n' \
                      f'\t"registration_start_date":"{date}",\n' \
                      f'\t"registration_end_date":"{date + timedelta(days=7)}",\n' \
                      f'\t"msg_id":{msg.id},\n' \
                      f'\t"emoji":"🛡"\n' \
                      '}'
            fout.write(out_str)

        await self.bot.pool.execute(f'DROP TABLE IF EXISTS tournament_{self.recent_tournament_data["id"]}')
        await self.bot.pool.execute(f'CREATE TABLE tournament_{tourny_id}('
                                    f'user_id bigint PRIMARY KEY,'
                                    f'ign varchar(20) NOT NULL,'
                                    f'pow_lvl int NOT NULL,'
                                    f'sup_prct DECIMAL(5,2) NOT NULL,'
                                    f'curr_team_id varchar(2),'
                                    f'wins smallint,'
                                    f'losses smallint,'
                                    f'status varchar(1)'
                                    f')')
        await ctx.send(f'Done creating table: ``tournament_{tourny_id}``')

        self.recent_tournament_data = json.loads(out_str)
        await msg.add_reaction('🛡')

    @commands.command()
    async def leavetournament(self, ctx):
        user_id = ctx.author.id
        await self.bot.pool.execute(f'DELETE FROM tournament_{self.recent_tournament_data["id"]} WHERE user_id={ctx.author.id}')
        await self.bot.get_user(user_id).send("You have unregistered from the upcoming **OPBR Tournament**")

    
    async def create_teams(self, registered_member_ids):
        pow_levels = registered_member_ids[0:len(registered_member_ids)]["pow_lvl"]
        precentile_25 = np.percentile(pow_levels, 25)
        percentile_50 = np.percentile(pow_levels, 50)
        percentile_75 = np.percentile(pow_levels, 75) ...............................................pswdefl[sdpflsdf]



    @commands.command()
    @commands.is_owner()
    async def maketeams(self, ctx):
        # TODO: Team making algorithm
        registered_member_ids = await self.bot.pool.fetch(f'SELECT id, pow_lvl FROM tournament_{self.recent_tournament_data["id"]} WHERE NOT losses > 2 ')

        
        teams = await create_teams(registered_member_ids)




def setup(bot):
    bot.add_cog(Tournament(bot))


