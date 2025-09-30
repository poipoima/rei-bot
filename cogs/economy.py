from models.User import User

class Economy(commands.GroupCog, name="economy", description="economy commands"):
    def __init__(self, bot): 
        self.bot = bot

    @app_commands.command(name="wallet", description="Check the wallet.")
    async def wallet(self, interaction: discord.Interaction):
        localUser = User.first_or_create(discord_id=interaction.user.id)
        localUser = User.first_or_create(discord_id=interaction.user.id)
    
        embed = discord.Embed(
            title="Economy",
            description=f"""💎 {localUser.money}
            🔹 {localUser.shards}""",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.choices(variant=[
        Choice(name='Gems', value=1),
        Choice(name='Shards', value=2),
    ])
    @app_commands.command(name="transfer", description="Transfer money.")
    async def transfer(self, interaction: discord.Interaction, member: discord.Member, number: int, variant: int):
        firstUser = User.first_or_create(discord_id=interaction.user.id)
        firstUser = User.first_or_create(discord_id=interaction.user.id)

        secondUser = User.first_or_create(discord_id=member.id)
        secondUser = User.first_or_create(discord_id=member.id)


        if( number < 0 ):
            embed = discord.Embed(
                title="Economy",
                description=f"Can't be smaller than zero.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)
            return


        if( variant == 1 ):
            if( firstUser.money-number < 0 ):
                embed = discord.Embed(
                    title="Economy",
                    description=f"Have no enough money.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)

                await interaction.response.send_message(embed=embed)
                return

            firstUser.money -= number
            firstUser.save()
            
            secondUser.money += number
            secondUser.save()

            embed = discord.Embed(
                title="Economy",
                description=f"Transfered 💎 {number}",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            if( firstUser.shards-number < 0 ):
                embed = discord.Embed(
                    title="Economy", 
                    description=f"Have no enough shards.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)

                await interaction.response.send_message(embed=embed)
                return

            firstUser.shards -= number
            firstUser.save()
            
            secondUser.shards += number
            secondUser.save()

            embed = discord.Embed(
                title="Economy",
                description=f"Transfered 🔹 {number}",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
