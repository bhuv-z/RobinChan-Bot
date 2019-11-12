import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import os
from io import BytesIO
title = []
role_list = []
reaction_list = []
gif_list = []

currPath = os.getcwd()
cogsPath = currPath + "\\cogs\\"
filepath = os.path.join(cogsPath, "reactionrole[wait_for]Contents.txt")


# ---------------------------------Load Reactions And Roles------------------------------------#
reactions_roles_list = open(filepath, 'r+')
lines = reactions_roles_list.read().split("\n")
num_roles = len(lines)

for i in range(0, num_roles):
    quads = lines[i].split("; ")
    title.append(quads[0])
    role_list.append(int(quads[1]))
    reaction_list.append(quads[2])
    gif_list.append(quads[3])
# ---------------------------------END Load Reactions And Roles---------------------------------#


class ReactionRoleWF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=266400, type=BucketType.user)
    async def role(self, ctx):
        guild = ctx.guild

        def _random_hex():
            return __import__("random").randint(0x000000, 0xFFFFFF)

        react_embed = discord.Embed(
            title="React to assign yourself the role that corresponds with the following colors",
            description="You can change your role again in 3 days, 2 hours",
            color=_random_hex()
        )
        react_embed.set_author(name="Assign a role", icon_url=self.bot.user.avatar_url)
        react_embed.set_image(url='https://i.imgur.com/TfIXKe6.png')
        react_embed.set_footer(text='Use ➡ to navigate through reaction pages')

        msg = await ctx.send(embed=react_embed)

        def check(reaction, user):
            if user == ctx.message.author and reaction.message.id == msg.id and \
                    ((str(reaction.emoji).replace('<', '').replace('>', '') in reaction_list)
                     or str(reaction.emoji) == '➡' or str(reaction.emoji) == '⬅'):
                return True

        async def react(ct, temp_list, recur_count):
            for i in range(ct, ct + 18):
                try:
                    if i <= 19 * recur_count:
                        await msg.add_reaction(emoji=reaction_list[i])
                        temp_list.append(reaction_list[i])
                        ct += 1
                        i += 1
                except IndexError:
                    break
            if ct > 18:
                await msg.add_reaction(emoji='⬅')
            if ct % 18 == 0:
                await msg.add_reaction(emoji='➡')
            return temp_list

        async def remove_reactions(message, member, temp_list):  # | *members to mention multiple members
            await message.remove_reaction('➡', member)  # | (*args)
            await message.remove_reaction('➡', ctx.message.author)
            await message.remove_reaction('⬅', member)
            await message.remove_reaction('⬅', ctx.message.author)

            for i in range(len(temp_list) - 1, -1, -1):
                await message.remove_reaction(temp_list[i], member)

        start_count = 0
        temp_list = []
        try:
            async def reaction_recursion(ct, temp_list, recur_count=0):
                recur_count += 1
                temp_list.clear()
                ct = len(await react(ct, temp_list, recur_count))
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                if str(reaction.emoji) == '➡':
                    await remove_reactions(msg, self.bot.user, temp_list)
                    reaction = await reaction_recursion(ct, temp_list, recur_count)
                if str(reaction.emoji) == '⬅':
                    await remove_reactions(msg, self.bot.user, temp_list)
                    reaction = await reaction_recursion(ct - (ct % 18), temp_list, recur_count)
                return reaction

            reaction = await reaction_recursion(start_count, temp_list)

            reaction_str = str(reaction.emoji).replace('<', '').replace('>', '')
        except asyncio.TimeoutError:
                await ctx.send("Next time react faster")
                self.bot.get_command("role").reset_cooldown(ctx)
        else:
            for j in range(0, num_roles):
                if reaction_str == reaction_list[j]:
                    role_added = role_list[j]

                    selected_role = guild.get_role(int(role_added))
                    if selected_role in ctx.author.roles:       # Checks if user already has role and notifies them
                        self.bot.get_command("role").reset_cooldown(ctx)
                        await ctx.send("%s you already have the role" % ctx.author.mention)
                        return      # Returns out of the function to prevent assigning and deleting roles

                    await assign_role(ctx, guild, role_added) # assigns role
                    welcome_gif = gif_list[j]
                    welcome_embed = discord.Embed(color=selected_role.color)
                    welcome_embed.set_image(url=welcome_gif)
                    await ctx.send("%s has joined the **%s**" % (ctx.message.author.mention,
                                                                 guild.get_role(role_added)), embed=welcome_embed)
                elif guild.get_role(role_list[j]) in ctx.author.roles:
                    await delete_role(ctx, guild, role_list[j])
                j += 1

    @commands.command()
    @commands.has_any_role(411773692717170688, 428942880443334657)
    async def newrole(self, ctx, *, arg):
        new_role = None
        new_emoji = None
        try:
            input = arg.split("; ")
            role_name = input[0].title()
            role_color = input[1].lstrip('#')
            rgb = "{}".format(tuple(int(role_color[i:i+2], 16) for i in (0, 2, 4)))
            rgb = rgb.replace('(', '').replace(')', '').split(", ")
            r = int(rgb[0])
            g = int(rgb[1])
            b = int(rgb[2])
            new_role = await ctx.guild.create_role(name=role_name, color=discord.Color.from_rgb(r, g, b))

            await ctx.send("Role Created!\n\n__**Emoji**__\nUpload the image to be used as the "
                           "role's reaction emote")

            def check(m):
                if m.author == ctx.message.author and m.channel == ctx.message.channel:
                    return True

            msg = await self.bot.wait_for('message', check=check)

            guild_for_emote = self.bot.get_guild(531596210587435045)  # RobinChanEmotes-1

            emoji_bytes = BytesIO()
            await msg.attachments[0].save(emoji_bytes)
            emoji_name = role_name

            new_emoji = await guild_for_emote.create_custom_emoji(name=emoji_name.replace(' ', ''), image=emoji_bytes.getvalue())
            emoji_str = str(new_emoji).replace('<', '').replace('>', '')
            role_str = str(new_role.id)

            await ctx.send("The emoji has been added to *%s* `name:` **%s**  `emoji:` %s" % (guild_for_emote.name, new_emoji.name,
                                                                                             str(new_emoji)))

            await ctx.send("Now add a welcome gif for the role")
            welcome_gif = await self.bot.wait_for('message', check=check)

            reactions_roles_list.write("\n" + role_name + "; " + role_str + "; " + emoji_str + "; " +
                                       welcome_gif.content)
            reactions_roles_list.flush()
            await ctx.send("Role added to the command ^-^")

        except Exception:
            if new_role is not None:
                await new_role.delete()
            if new_emoji is not None:
                await new_emoji.delete()
            await ctx.send("Oops Something went wrong, Try again")

    @commands.command()
    @commands.has_any_role(411773692717170688, 428942880443334657)
    async def rolecount(self, ctx):

        def role(role_id):
            return ctx.guild.get_role(role_id)

        role_data = '```java\nMember count of command roles\n\n'

        for i in range(0, num_roles):
            # role_data += '%s:   %s\n' % (role(role_list[i]).name.title(), str(len(role(role_list[i]).members)))
            role_data += '+{}+\n'.format('-' * 24)
            role_data += '|{:>19} | {:<2}|\n'.format(role(role_list[i]).name.title(), len(role(role_list[i]).members))
        role_data += '+{}+\n```'.format('-' * 24)

        await ctx.send(role_data)



async def assign_role(ctx, guild, roleid):
    return await ctx.author.add_roles(guild.get_role(roleid))


async def delete_role(ctx, guild, roleid):
    return await ctx.author.remove_roles(guild.get_role(roleid))


def setup(bot):
    bot.add_cog(ReactionRoleWF(bot))
