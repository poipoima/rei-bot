# Created with magi tool
import discord
from discord.ext import commands
from discord import app_commands
from random import choice
import asyncio
from models.User import User

class Casino(commands.GroupCog, name="casino", description="casino commands"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spin", description="Spin a wheel")
    async def spin(self, interaction: discord.Interaction, amount: int):
        localUser = User.first_or_create(discord_id=interaction.user.id)

        if amount <= 0:
            embed = discord.Embed(
                title="⚠️ Invalid Bet",
                description="Your bet should be **more than zero**.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if amount > localUser.money:
            embed = discord.Embed(
                title="💸 Not Enough Balance",
                description="You don't have enough 💎 to place that bet.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        spinning_embed = discord.Embed(
            title="🎡 Spinning the Wheel...",
            description="Please wait a moment while the wheel spins... ⏳",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=spinning_embed)
        message = await interaction.original_response()

        await asyncio.sleep(3)

        multiplier = choice([0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        winnings = amount * multiplier
        localUser.money -= amount
        localUser.money += winnings
        localUser.save()
                
        result_embed = discord.Embed(
            title="🎰 Slot Spin Result",
            description=f"You bet 💎 **{amount}**\n"
                        f"You spun a **{multiplier}x**\n\n"
                        f"You won 💎 **{winnings}**!",
            color=discord.Color.gold()
        )
        result_embed.set_footer(text="Good luck on your next spin! 🍀")

        await message.edit(embed=result_embed)
