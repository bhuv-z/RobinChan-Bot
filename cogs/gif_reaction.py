import discord
from discord.ext import commands
import random


shocked_gif = ["https://media.giphy.com/media/Ai8iZqHx2i0fK/giphy.gif",
               "https://media.giphy.com/media/Ai8iZqHx2i0fK/giphy.gif",
               "https://media.giphy.com/media/KueK59JZtbcSA/giphy.gif",
               "https://media.giphy.com/media/Wp7YE6DQ5MwPm/giphy.gif",
               "https://media.giphy.com/media/qVXMA8p0X0vPW/giphy.gif",
               "https://thumbs.gfycat.com/BlandSpotlessHawk-small.gif",
               "http://i.imgur.com/Wz590fs.gif",
               "https://i.pinimg.com/originals/5e/c3/a0/5ec3a0ca9f8bb0d5ebae2119aa47627b.gif"]
shocked_exps = ['😱', 'nani', '?!', 'wtf', 'omg']

angry_gif = ["https://media1.tenor.com/images/be01e865ad1b015090604643dcabee91/tenor.gif?itemid=5235529",
             "https://i.pinimg.com/originals/7e/bd/6e/7ebd6ee8d522a989102111c82088507a.gif",
             "https://media1.tenor.com/images/65d5a034d47d2050a9568f30bfdd5030/tenor.gif?itemid=5378956",
             "https://pa1.narvii.com/5868/f350cfeb933714017e0e27e657af05f45fccc71d_hq.gif",
             "https://media.giphy.com/media/1xoZG8nP9zkYrM50VE/giphy.gif",
             "https://media.giphy.com/media/3CUakp0bLq0l9hQWmn/giphy.gif"]
angry_exps = ['reee', '😠', '😡', 'smfh']

crying_gif = ["https://media.giphy.com/media/3s1B6FF1EjvFe/giphy.gif",
              "https://thumbs.gfycat.com/PartialThunderousDeermouse-small.gif",
              "https://thumbs.gfycat.com/CorruptImpoliteGlowworm-small.gif",
              "https://media.giphy.com/media/25R4A9jIviUOiinnk8/giphy.gif"]
crying_exps = ['i cri', '😭', '😢', 'welp']

cute_gif = ["https://media1.tenor.com/images/2893952919f7776b041e0c7c4dd7dea4/tenor.gif?itemid=3570258",
            "https://i.pinimg.com/originals/eb/df/8e/ebdf8ebe30b6ba961642769d5191bc77.gif"]
cute_exps = ['cute', 'kyot', 'kawaii']

scared_gif = ["https://thumbs.gfycat.com/AptEmbarrassedEarwig-small.gif",
              "https://thumbs.gfycat.com/YoungCompetentButterfly-size_restricted.gif"]
scared_exps = ['creepy', 'weird']

laugh_gif = ["https://i.pinimg.com/originals/13/38/08/13380886c6ba966f6a2183d3731cadb8.gif",
             "https://media.giphy.com/media/UbQQK3SUZxCQ8/giphy.gif",
             "https://data.whicdn.com/images/208232507/original.gif",
             "https://thumbs.gfycat.com/FarawayOrderlyDeinonychus-small.gif"]
laugh_exps = ['lmaoo', 'loool', 'hahaha', 'keek']

tease_gif = []
tease_exps = []

smile_gif = []
smile_exps = []

pat_gif = []
pat_exps = []

annoyed_gif = []
annoyed_exps = []


class Gif_Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        def embed(author, gif, reaction):
            embed = discord.Embed(color=0x38393a)
            embed.set_author(name=f'{author} {reaction}')
            embed.set_image(url=gif)
            return embed

        author = message.author.name
        if message.content in shocked_exps:
            gif = random.choice(shocked_gif)
            await message.channel.send(embed=embed(author, gif, 'is shocked   （＊〇□〇）……！'))
            return
        elif message.content in angry_exps:
            gif = random.choice(angry_gif)
            await message.channel.send(embed=embed(author, gif, 'is pissed!!!!  （╬ಠ益ಠ)'))
            return
        elif message.content in crying_exps:
            gif = random.choice(crying_gif)
            await message.channel.send(embed=embed(author, gif, 'weeps T_T'))
            return
        elif message.content in cute_exps:
            gif = random.choice(cute_gif)
            await message.channel.send(embed=embed(author, gif, 'is awestruck  ( *’ω’* )'))
            return
        elif message.content in scared_exps:
            gif = random.choice(scared_gif)
            await message.channel.send(embed=embed(author, gif, 'is scared ( ⚆ _ ⚆ )'))
            return
        elif message.content in laugh_exps:
            gif = random.choice(laugh_gif)
            await message.channel.send(embed=embed(author, gif, 'be like (๑˃́ꇴ˂̀๑)'))
            return


def setup(bot):
    bot.add_cog(Gif_Reaction(bot))
