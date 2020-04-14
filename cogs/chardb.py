import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import re
import traceback


char_names = []


class opbrDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def select(self, ctx, *, args):
        try:
            print(f'ADMIN QUERY: {args}')
            qargs = re.findall('(.*)(?= from)', args)
            qargs = qargs[0].split(', ')
            if args.split(' ')[0] is not '*':
                records = await self.bot.pool.fetch(f'SELECT {args}')
                out = ''
                for i in range(0, len(records)):
                    for q in range(0, len(qargs)):
                        if qargs[q].lower() == 'id':
                            out += '%03d | ' % records[i][f"{qargs[q]}"]
                        else:
                            out += '%s | ' % str(records[i][f"{qargs[q]}"])

                    out += '\n'
                # out += '%03d | %s\n' % (records[i]["id"], records[i]["name"])
                await ctx.send(f'```{out}```')
            else:
                await ctx.send('You can not query all records')
        except Exception as e:
            err = (traceback.format_exc()).replace("BHUVANESHWAR", "user")
            await ctx.send(f'```{e}\n\n{err}```')

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx, *, args):
        try:
            print(f'ADMIN UPDATE: {args}')
            await self.bot.pool.execute(f"UPDATE {args}")
            await ctx.send(f"``Done``")
        except Exception as e:
            err = (traceback.format_exc()).replace("USER", "user")
            await ctx.send(f'```{e}\n\n{err}```')

    @commands.command()
#    @commands.cooldown(1,60,BucketType.user)
    async def art(self, ctx, args):
        records = await self.bot.pool.fetch(f"SELECT id, name, alias, art from chars "
                                            f"WHERE name LIKE '{args.title()}%' OR "
                                            f"name LIKE '% {args.title()}%' ORDER BY id")
        if records:
            await self.print_char_list(args.title(), records, ctx)  # Print unit list and ask user to reply with id

            def check(m):
                if m.author == ctx.message.author and m.channel == ctx.message.channel:
                    return True

            reply = await self.bot.wait_for('message', check=check, timeout=10)
            id = int(float(reply.content))
            rec_ids = await self.load_queried_char_ids(records)
            if id in rec_ids:
                index = rec_ids.index(id)
                art_embed = discord.Embed(title=records[index]["alias"], color=0x42d7f4)
                art_embed.set_author(name=records[index]["name"])
                art_embed.set_image(url=records[index]["art"])
                await ctx.send(embed=art_embed)
            else:
                return await ctx.send('``Invalid ID``')
        else:
            return await ctx.send('``Invalid Name: Check for typos``')

    @commands.command()
#    @commands.cooldown(1, 60, BucketType.user)
    async def charlist(self, ctx, *, args):
        char_list = await self.bot.pool.fetch(f"SELECT id, alias FROM chars WHERE name LIKE '{args.title()}%' OR "
                                              f"name LIKE '% {args.title()}%' ORDER BY id")
        out = f"Here list of {args}'s units:\n\n"
        for i in range(0, len(char_list)):
            out += '%03d.   %3s\n' % (char_list[i]["id"], char_list[i]["alias"])
        await ctx.send(f'```{out}```')

    @commands.command()
#    @commands.cooldown(1, 60, BucketType.user)
    async def char(self, ctx, *, args):
        if args.isdigit():
            qarg = int(float(args))
        else:
            char_list = await self.bot.pool.fetch(f"SELECT id, name, alias FROM chars "
                                                  f"WHERE name LIKE '{args.title()}%' OR "
                                                  f"name LIKE '% {args.title()}%' ORDER BY id")
            if not char_list:
                return await ctx.send('``Enter a valid name``')
            await self.print_char_list(args.title(), char_list, ctx)

            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel

            resp = await self.bot.wait_for("message", check=check, timeout=10)

            char_list_ids = await self.load_queried_char_ids(char_list)

            if resp.content.isdigit() and int(float(resp.content)) in char_list_ids:
                qarg = int(float(resp.content))
            else:
                return await ctx.send(f"``Enter a valid id``")

        char = await self.bot.pool.fetch(f"SELECT id, init_rarity, name, class, elem, alias, hp, atk, def, tot_pow, "
                                         f"crit, char_trait, trait_1, trait_2, frag, art, f2p FROM chars "
                                         f"WHERE id={int((float(qarg)))}")
        if not char:
            return await ctx.send(f"``Enter a valid id``")

        char = char[0]
        char_embed = discord.Embed(title='%s    %s' % (char["alias"], '[F2P]' if char["f2p"] else ''),
                                   description=char["char_trait"] if char["char_trait"] != "NA" else '',
                                   color=self.elem_color_picker(char["elem"].lower()))
        char_embed.set_author(name=char["name"], icon_url=self.class_icon(char["elem"], char["class"]))
        char_embed.set_footer(text='%03d' % char["id"])
        char_embed.set_thumbnail(url=char["frag"])
        char_embed.set_image(url=char["art"])
        char_embed.add_field(name='Class', value=char["class"])
        char_embed.add_field(name='Element', value=char["elem"])
        char_embed.add_field(name='Starting Rarity', value='%d★' % char["init_rarity"], inline=False)
        char_embed.add_field(name='Total Power', value=char["tot_pow"], inline=False)
        char_embed.add_field(name='HP', value=char["hp"])
        char_embed.add_field(name='ATK', value=char["atk"])
        char_embed.add_field(name='DEF', value=char["def"])
        char_embed.add_field(name='CRIT', value=f'{char["crit"] * 100}%')
        char_embed.add_field(name='Trait 1', value=char["trait_1"], inline=False)
        char_embed.add_field(name='Trait 2', value=char["trait_2"], inline=False)

        await ctx.send(embed=char_embed)

    @staticmethod
    async def load_queried_char_ids(records):
        check_list = []
        for i in range(0, len(records)):
            check_list.append(records[i]["id"])
        return check_list

    @staticmethod
    async def print_char_list(name, records, ctx):
        out = ''
        for i in range(0, len(records)):
            out += '[**%03d**] - %s: %s\n' % (records[i]["id"], records[i]["name"], records[i]["alias"])

        embed = discord.Embed(title='Reply with the ID of the unit you would like to view', color=0x00e5ff)
        embed.add_field(name=f"Here is a list of {name}'s units", value=f'\n{out}')
        await ctx.send(embed=embed)

    @staticmethod
    def elem_color_picker(elem):
        if elem == "green":
            return 0x03766d
        elif elem == "red":
            return 0x920010
        else:
            return 0x043892

    @staticmethod
    def class_icon(elem, cls):
        cls_elem = {}
        cls_elem["RedRunner"] = 'https://i.ibb.co/bvvksgB/0008-icon-role-getter.png'
        cls_elem["BlueRunner"] = 'https://i.ibb.co/R7QxZLg/0005-icon-role-getter-copy-2.png'
        cls_elem["GreenRunner"] = 'https://i.ibb.co/KDwX85j/0002-icon-role-getter.png'
        cls_elem["RedDefender"] = 'https://i.ibb.co/LCH4b2D/0006-icon-role-defender-copy-2.png'
        cls_elem["BlueDefender"] = 'https://i.ibb.co/pZfKPsv/0003-icon-role-defender-copy.png'
        cls_elem["GreenDefender"] = 'https://i.ibb.co/HP13DJ6/0000-icon-role-defender.png'
        cls_elem["RedAttacker"] = 'https://i.ibb.co/6nrZXrd/0007-icon-role-attacker-copy-2.png'
        cls_elem["BlueAttacker"] = 'https://i.ibb.co/4JHyLKw/0004-icon-role-attacker.png'
        cls_elem["GreenAttacker"] = 'https://i.ibb.co/j3cKk18/0001-icon-role-attacker-copy.png'
        return cls_elem[elem + cls]

    # @staticmethod
    # def wallapapers(imgurl)

def setup(bot):
    bot.add_cog(opbrDB(bot))
