# Created with magi tool
import discord
from discord.ext import commands
from discord import app_commands
from random import choice
import asyncio
from models.User import User

class Cave(commands.GroupCog, name="cave", description="cave commands"):
    def __init__(self, bot):
        self.bot = bot
        self.active_miners = set()

    @app_commands.command(name="mine", description="Mine for gems")
    async def mine(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id in self.active_miners:
            embed = discord.Embed(
                title="⛏️ Already Mining",
                description="You're already mining gems, please wait until it finishes!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.active_miners.add(user_id)

        try:
            localUser = User.first_or_create(discord_id=user_id)

            mining_gifs = [
                "https://gifdb.com/images/high/anime-character-mining-wrolocv0ejbwthx4.gif",
                "https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyamV2bW0yb2M3bTVnYjNhaXhscjRueWxzMmZvbzU3ZnRiZDdrN3k3NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/6fDQ3k4IOqnEA/giphy.gif",
                "https://tenor.com/view/mine-doge-gif-24806628"
            ]

            reward_gifs = [
                "https://i.pinimg.com/originals/ee/dc/ee/eedcee0dc838d6116006a08b34079ca1.gif",
                "https://i.pinimg.com/originals/04/cb/1c/04cb1c53501ffe8293dc1b12328ae25f.gif",
                "https://media.tenor.com/OBC8G0kPA2MAAAAM/gem-gemstone.gif"
            ]

            nothing_gifs = [
                "https://media0.giphy.com/media/v1.Y2lkPTZjMDliOTUydmhleWM4YmJ3aWcxa3E5Y2o5N3BoMG44anN1a2Zvc2owdXdubjBndiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ujZtlj1Y7wXyE/source.gif",
                "https://i.pinimg.com/originals/d6/20/f4/d620f43fcc7dba0a79712b6d41a8ed2d.gif",
                "https://i.pinimg.com/originals/ef/3e/b8/ef3eb8f49a88c5de84a476f7e704ee17.gif"
            ]

            import random
            mining_gif = random.choice(mining_gifs)
            reward_gif = random.choice(reward_gifs)
            nothing_gif = random.choice(nothing_gifs)

            mining_embed = discord.Embed(
                title="⛏️ Mining in progress...",
                description="You're digging for gems... please wait... 💎",
                color=discord.Color.gold()
            )
            mining_embed.set_image(url=mining_gif)

            await interaction.response.send_message(embed=mining_embed)
            message = await interaction.original_response()

            await asyncio.sleep(3)

            mined_gems = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            if mined_gems == 0:
                result_embed = discord.Embed(
                    title="💎 Mining Result",
                    description="You found no gems...",
                    color=discord.Color.red()
                )
                result_embed.set_image(url=nothing_gif)

                await message.edit(embed=result_embed)
                return

            localUser.money += mined_gems
            localUser.save()

            result_embed = discord.Embed(
                title="💎 Mining Result",
                description=f"You mined **{mined_gems}** shiny gems!",
                color=discord.Color.green()
            )
            result_embed.set_image(url=reward_gif)

            await message.edit(embed=result_embed)

        finally:
            self.active_miners.discard(user_id)
