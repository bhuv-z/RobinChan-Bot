import discord
from discord.ext import commands
import traceback
import math
import PIL
from PIL import Image, ImageFont, ImageDraw
import aiohttp
from functools import partial   # Prepare new function to run in executor
from io import BytesIO      # Convert bytes into file-like bytes system
from typing import Union       # extra
import time
import asyncpg
import asyncio
import threading
import random


member_ids = []
exp_arr = [163.0, 169.0, 176.0, 182.0, 189.0, 196.0, 203.0, 210.0, 218.0, 225.0, 233.0, 240.0, 248.0, 256.0, 264.0,
           272.0, 281.0, 289.0, 298.0, 306.0, 315.0, 324.0, 333.0, 342.0, 352.0, 361.0, 371.0, 380.0, 390.0, 400.0,
           410.0, 420.0, 431.0, 441.0, 452.0, 462.0, 473.0, 484.0, 495.0, 506.0, 518.0, 529.0, 541.0, 552.0, 564.0,
           576.0, 588.0, 600.0, 613.0, 625.0, 638.0, 650.0, 663.0, 676.0, 689.0, 702.0, 716.0, 729.0, 743.0, 756.0,
           770.0, 784.0, 798.0, 812.0, 827.0, 841.0, 856.0, 870.0, 885.0, 900.0, 915.0, 930.0, 946.0, 961.0, 977.0,
           992.0, 1008.0, 1024.0, 1040.0, 1056.0, 1073.0, 1089.0, 1106.0, 1122.0, 1139.0, 1156.0, 1173.0, 1190.0,
           1208.0, 1225.0, 1243.0, 1260.0, 1278.0, 1296.0, 1314.0, 1332.0, 1351.0, 1369.0, 1388.0]
blacklisted_channels = []

# exp_drop_time_delay = [8400, 6000, 3600]
exp_drop_time_delay = [50, 60, 70]
exp_drop_value = [50, 20, 10]
#   TODO: Add goodies event
#   TODO: Add Missions (MAYBE)


class RankingAndRewards(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.pool
        self.session = aiohttp.ClientSession(loop=bot.loop)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.pool.execute('CREATE TABLE IF NOT EXISTS activity_ranking('
                                    'id bigint PRIMARY KEY NOT NULL, msg_count bigint NOT NULL, level smallint NOT NULL,'
                                    'exp int NOT NULL, badges int[], bounty int NOT NULL)')
        await self.bot.pool.execute('CREATE TABLE IF NOT EXISTS badges('
                                    'id serial PRIMARY KEY NOT NULL, name varchar(30) NOT NULL, description text NOT NULL, '
                                    'img varchar(200) NOT NULL, level smallint NOT NULL, badge_set varchar(200) NOT NULL)')
        await self.bot.pool.execute("CREATE TABLE IF NOT EXISTS blacklisted_channels(id bigint PRIMARY KEY NOT NULL,"
                                    "blacklisted_by bigint NOT NULL)")
        print(f'--Ranking, Badges and Blacklist Tables Created')
        
        blacklisted_channel_records = await self.bot.pool.fetch('SELECT id from blacklisted_channels')
        for i in blacklisted_channel_records:
            blacklisted_channels.append(i["id"])
        print(f'--All blacklisted channels loaded: {blacklisted_channels}')

        # await self.exp_drops(self, self.bot.get_channel(411996358338281474), 0)

    @commands.Cog.listener()
    async def on_message(self, message):    # Listen to message and add exp etc.
        if not message.author.bot and message.channel.id not in blacklisted_channels:
            # Add 1 exp per msg
            member = await self.bot.pool.fetch(f"SELECT * from activity_ranking WHERE id='{message.author.id}'")
            if member:  # change to if id in member_ids if connecting to db becomes slow
                exp_up = member[0]["exp"] + 1
                msg_count_up = member[0]["msg_count"] + 1
                await self.bot.pool.execute(f"UPDATE activity_ranking SET exp={exp_up}, msg_count={msg_count_up} "
                                            f"WHERE id={message.author.id}")

                # Using Formula to level up
                if exp_up == round(pow(((member[0]["level"] + 51)/4), 2)):
                    member_updated = await self.level_up(message.author.id, member)
                    # Level up image processing. Make Function if needed
                    async with message.channel.typing():
                        # create partial function so we don't have to stack the args in run_in_executor
                        fn = partial(self.level_img, member_updated[0]["level"])
                        # this runs the processing in an executor, stopping it from blocking the thread loop.
                        # as we already seeked back the buffer in the other thread, we're good to go
                        out_buffer = await self.bot.loop.run_in_executor(None, fn)
                        # file for output
                        file = discord.File(filename="level_up.png", fp=out_buffer)
                        await message.channel.send(content=f'{message.author.mention} You have leveled up', file=file)

                    #   Assign badge upon reaching badge level
                    if member_updated[0]["level"] % 10 == 0 or member_updated[0]["level"] == 2:
                        await self.rankBadgeAssign(message.channel, member, member_updated[0]["level"])
            else:

                await self.bot.pool.execute(f"INSERT INTO activity_ranking (id, msg_count, level, exp, bounty) "
                                            f"VALUES ({message.author.id}, 0, 0, 0, 0)")

    @commands.command()
    @commands.is_owner()
    async def insert(self, ctx, *, args):   # INSERT Rows into the table
        try:
            await self.bot.pool.execute(f'INSERT {args}')
            await ctx.send('Done Inserting')
        except Exception as e:
            await ctx.send(f"```{e}\n\n{(traceback.format_exc()).replace('BHUVANESHWAR', 'user')}```")

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, arg):
        try:
            insert = await self.bot.pool.execute(f'INSERT INTO blacklisted_channels VALUES({int(arg)}, {ctx.author.id})')
            blacklisted_channels.append(int(arg))
            await ctx.send(f'```{insert}```')
        except Exception as e:
            await ctx.send(f"```{e}```")

    @commands.command()
    async def bulletin(self, ctx):
        try:
            out = '```Swift\n📊 %2s\n\n' % 'Leader-board'
            records = await self.bot.pool.fetch(f'SELECT * from activity_ranking ORDER BY msg_count DESC LIMIT 10')
            for i in range(0, 10):
                member = self.bot.get_user(records[i]["id"])
                out += '{:>4}  {}\n{:>15s} {}{:>15} {}{:>15}  ℬ {}\n\n'.format(f'{[i+1]}', f'{str(member).title()}', 'Level:', records[i]["level"],
                                                                               'Messages:', records[i]["msg_count"], 'BOUNTY:', records[i]["bounty"])

            member_rank, bounty = await self.get_member_rank(ctx.author.id)
            out += f"{'-' *  70}\n👀 Your_Stats\n     Rank: {member_rank}\n     Bounty: {bounty}\n```"

            await ctx.send(out)
        except IndexError:
            await ctx.send('Wait till at least 10 members send a message')

    @commands.command()
    async def poster(self, ctx, *, member: discord.Member = None):
        # If arg is user, process that user else process author

        member = member or ctx.author
        if member.bot is True:
            return
        async with ctx.typing():
            record = await self.bot.pool.fetch(f'SELECT level, msg_count, bounty, exp, badges FROM activity_ranking WHERE id={member.id}')
            avatar_bytes = await self.get_avatar(member)
            member_rank, bounty_not_used = await self.get_member_rank(member.id)
            # adding to partial
            fn = partial(self.poster_img, avatar_bytes, member.display_name, record, member_rank)
            out_buffer = await self.bot.loop.run_in_executor(None, fn)
            # create the file
            file = discord.File(filename=f'{member.display_name}_poster.png', fp=out_buffer)

            msg = await ctx.send(file=file)
        try:
            if record[0]["badges"] is not None:  # if user has badges add 🅱 reaction
                await msg.add_reaction(emoji='🅱')

                def check(reaction, user):  # check user and reaction
                    if user == ctx.message.author and str(reaction.emoji) == '🅱' and reaction.message.id == msg.id:
                        return True
                await self.bot.wait_for('reaction_add', check=check, timeout=20)    # wait for reaction

                badge_count = len(record[0]["badges"])  # use badge count for badge id
                badge_set = await self.bot.pool.fetch(f'SELECT badge_set FROM badges WHERE id={badge_count}')
                badge_set_embed = discord.Embed(title=f"{member.display_name}'s badges", color=0x38393a)
                badge_set_embed.set_image(url=badge_set[0]["badge_set"])
                await ctx.send(embed=badge_set_embed)

        except asyncio.TimeoutError:
            return

    # ---------------------- Functions ----------------------------------------------------------------------------#
    async def level_up(self, mem_id, member):  # The level up process as a function
        await self.bot.pool.execute(f'UPDATE activity_ranking SET level={member[0]["level"] + 1}, '
                                    f'exp=0, bounty={member[0]["bounty"]+(member[0]["level"] + 1)*10000} WHERE '
                                    f'id={mem_id}')
        member_updated = await self.bot.pool.fetch(f"SELECT * from activity_ranking "
                                                   f"WHERE id={mem_id}")
        return member_updated

    async def rankBadgeAssign(self, channel, member, level):  # Assign badges every 10 levels
        badge_id = None
        color = None
        if level == 2:
            badge_id = 1
            color = 0x82483e
        elif level == 10:
            print('10')
        elif level == 20:
            print('20')
        elif level == 30:
            print('20')
        elif level == 40:
            print('20')
        elif level == 50:
            print('20')
        elif level == 60:
            print('20')
        elif level == 70:
            print('20')
        elif level == 80:
            print('20')
        elif level == 90:
            print('90')
        elif level == 100:
            print('100')
        try:
            badge_record = await self.bot.pool.fetch(f'SELECT * from badges WHERE id={badge_id}')
            await self.bot.pool.execute(f'UPDATE activity_ranking SET badges=array_append(badges, {badge_id}) '
                                        f'WHERE id={member.id}')
            badge_embed = discord.Embed(title=f'{member.name} You have received the badge: '
                                              f'{badge_record[0]["name"]}',
                                        description=f'{badge_record[0]["description"]}',
                                        color=color)
            badge_embed.set_image(url=f'{badge_record[0]["img"]}')
            return await channel.send(embed=badge_embed)
        except asyncpg.exceptions.UndefinedColumnError:
            await channel.send('``The badge for this level doesnt exist``')
        except Exception as e:
            await channel.send(f"```{e}```")

    @staticmethod
    def level_img(level) -> BytesIO:
        with Image.open("level_up_out.png") as level_up_img:
            draw = ImageDraw.Draw(level_up_img)
            font = ImageFont.truetype("Fonts/Bonard.ttf", 28)
            draw.text((80, 30), f'{level}', (255, 255, 255), font=font)

            out_buffer = BytesIO()
            level_up_img.save(out_buffer, 'png')
        out_buffer.seek(0)
        return out_buffer

    # async def on_level_up(self, message, member):
    #     member_updated = await self.level_up(message, member)
    #     # Level up image processing. Make Function if needed
    #     async with message.channel.typing():
    #         # create partial function so we don't have to stack the args in run_in_executor
    #         fn = partial(self.level_img, member_updated[0]["level"])
    #         # this runs the processing in an executor, stopping it from blocking the thread loop.
    #         # as we already seeked back the buffer in the other thread, we're good to go
    #         out_buffer = await self.bot.loop.run_in_executor(None, fn)
    #         # file for output
    #         file = discord.File(filename="level_up.png", fp=out_buffer)
    #         await message.channel.send(content=f'{message.author.mention} You have leveled up', file=file)
    #
    #     #   Assign badge upon reaching badge level
    #     if member_updated[0]["level"] % 10 == 0 or member_updated[0]["level"] == 2:
    #         await self.rankBadgeAssign(message, member_updated[0]["level"])

    async def get_member_rank(self, member_id):
        records = await self.bot.pool.fetch('SELECT id, bounty from activity_ranking ORDER BY msg_count DESC')
        for i in records:
            if records[records.index(i)]["id"] == member_id:
                return records.index(i) + 1, records[records.index(i)]["bounty"]

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        avatar_url = f"{user.avatar_url_as(format='png')}"
        async with self.session.get(url=avatar_url) as response:
            # read bytes from image in url
            avatar_bytes = await response.read()
        return avatar_bytes

    @staticmethod
    def poster_img(avatar_bytes: bytes, name: str, record, member_rank) -> BytesIO:
        # open url as img
        with Image.open(BytesIO(avatar_bytes)).resize((360, 360), Image.ANTIALIAS) as avatar_image:
            with Image.new('RGBA', (429, 606), (0, 0, 0, 0)) as base_bg:     # Create transparent base
                base_bg.paste(avatar_image, (37, 112))       # Paste avatar on base
                with Image.open('poster_image.png') as poster_img:  # open poster bg
                    base_bg.paste(poster_img, (0, 0), mask=poster_img)   # paste poster bg on base
                # add member name tp image
                font_size = 0
                for i in range(0, len(name)):
                    if 20 >= len(name) > 12:
                        font_size = 30
                    elif len(name) >= 21:
                        font_size = 20
                    else:
                        font_size = 50
                font = ImageFont.truetype("Fonts/AGaramondPro-Bold.otf", font_size)
                draw = ImageDraw.Draw(base_bg)
                nw, nh = draw.textsize(name.upper(), font=font)
                draw.text(((426-nw)/2, 456), name.upper(), font=font, fill=(28, 16, 12))
                # Add bounty to image
                font = ImageFont.truetype("Fonts/AGaramondPro-Regular.otf", 35)
                bounty_arr = str(record[0]["bounty"])
                bounty_str = ''
                for i in range(len(bounty_arr), 0, -1):
                    bounty_str += bounty_arr[len(bounty_arr) - i]
                    if (i - 1) % 3 == 0 and i - 1 != 0:
                        bounty_str += ' , '
                draw.text((75, 520), bounty_str, font=font, fill=(28, 16, 12))
                # add exp to image
                font = ImageFont.truetype("Fonts/Rockness.ttf", 27)
                exp_str = f'{record[0]["exp"]} / {round(pow(((record[0]["level"] + 51)/4), 2))}'
                draw.text((95, 569), exp_str, font=font, fill=(28, 16, 12))
                # add level to image
                font = ImageFont.truetype("Fonts/Rockness.ttf", 25)
                lvl_str = f'{record[0]["level"]}'
                lw, lh = draw.textsize(lvl_str, font=font)
                draw.text(((38-lw)/2, 220), lvl_str, font=font, fill=(28, 16, 12))
                # add rank to image
                # get rgb from bottom right corner pixel offset 20px from margin
                with avatar_image.convert('RGB') as avatar_image_rgb:
                    R, G, B = avatar_image_rgb.getpixel((330, 330))
                    luminance = (0.299*R + 0.587*G + 0.114*B)
                    # assign color based on luminance
                    if luminance > 160:
                        fill = 'black'
                    else:
                        fill = 'white'
                    font = ImageFont.truetype("Fonts/Rockness.ttf", 75)
                    rw, rh = draw.textsize(f'{member_rank}', font=font)  # layer height and width
                    with Image.new('RGBA', (rw + 50, rh + 50), (0, 0, 0, 0)) as rank_base:
                        rank_base_draw = ImageDraw.Draw(rank_base)
                        rank_base_draw.text((10, 10), f'{member_rank}', font=font, fill=fill)   # draw 10px offset from margin
                        rotated = rank_base.rotate(angle=30)
                        base_bg.paste(rotated, (385-rw, 270), mask=rotated)

                # output buffer
                out_buffer = BytesIO()
                base_bg.save(out_buffer, 'png')

        out_buffer.seek(0)

        return out_buffer

    # @staticmethod
    # async def exp_drops(self, channel, delay_interval):
    #
    #     # delay the next drop
    #     await asyncio.sleep(delay_interval)
    #
    #     if delay_interval > 0:
    #
    #         try:
    #             async with channel.typing():
    #                 exp_value = exp_drop_value[exp_drop_time_delay.index(delay_interval)]
    #                 expEmbed = discord.Embed(title='EXP Drop',
    #                                          description=f"Voila a **{exp_value} EXP** drop! Reply ``claimexp``")
    #                 expEmbed.set_thumbnail(url='https://i.imgur.com/gL6ZGgi.png')
    #                 await channel.send(embed=expEmbed)
    #
    #                 def check(m):
    #                     if m.channel == channel and m.content == "claimexp":
    #                         return True
    #
    #                 response = await self.bot.wait_for('message', check=check, timeout=20)
    #                 member = response.author
    #
    #                 # add exp to player db
    #                 member_record = await self.bot.pool.fetch(f"SELECT * FROM activity_ranking WHERE id={member.id}")
    #                 curr_exp = member_record[0]["exp"]
    #                 for i in range(1, exp_value):
    #                     curr_exp += i
    #                     await self.bot.pool.execute(f'UPDATE activity_ranking SET exp={curr_exp} WHERE id={member.id}')
    #                     if member_record[0]["exp"] == round(pow(((member_record[0]["level"] + 51) / 4), 2)):
    #                         member_updated = await self.level_up(member.id, member_record)
    #                         async with channel.typing():
    #                             fn = partial(self.level_img, member_updated[0]["level"])
    #                             out_buffer = await self.bot.loop.run_in_executor(None, fn)
    #                             file = discord.File(filename="level_up.png", fp=out_buffer)
    #                             await channel.send(content=f'{member.mention} You have leveled up', file=file)
    #                         #   Assign badge upon reaching badge level
    #                         if member_updated[0]["level"] % 10 == 0 or member_updated[0]["level"] == 2:
    #                             await self.rankBadgeAssign(channel, member, member_updated[0]["level"])
    #
    #                 await channel.send(f'{member.mention} just snatched that {exp_value} :sugoi:    __Total EXP:__ ***{curr_exp}***')
    #         except asyncio.TimeoutError:
    #             await channel.send('``The EXP drop was left unclaimed``')
    #
    #     # delay begin
    #     delay = random.choices(population=exp_drop_time_delay, weights=[0.2, 0.3, 0.5], k=1)
    #     print(delay)
    #     delay = delay[0]
    #
    #     task = asyncio.create_task(self.exp_drops(self, channel, delay))
    #     await task
    #     # TODO: HANDLE: TypeError: exp_drops() argument after ** must be a mapping, not TextChannel
    #     # TODO: HANDLE: TimeoutError Inside if


def setup(bot):
    bot.add_cog(RankingAndRewards(bot))


"""
import math
levels_array = []
x = 0
y =0
for i in range(51,150):
    x=round(pow((i/4),2))
    print(f'EXP @ {i}      = {x + 1}')
    y+=x
    levels_array.append(x)

print(levels_array)
print(y)
"""
