from models.User import User

class Economy(commands.GroupCog, name="economy", description="economy commands"):
    def __init__(self, bot): 
        self.bot = bot

    @app_commands.command(name="wallet", description="Check the wallet.")
    async def wallet(self, interaction: discord.Interaction):
        localUser = User.first_or_create(discord_id=interaction.user.id)
        localUser = User.first_or_create(discord_id=interaction.user.id)

        await interaction.response.send_message(f"Money = {localUser.money}")

    @app_commands.command(name="transfer", description="Transfer money.")
    async def transfer(self, interaction: discord.Interaction, member: discord.Member, number: int):
        firstUser = User.first_or_create(discord_id=interaction.user.id)
        firstUser = User.first_or_create(discord_id=interaction.user.id)

        secondUser = User.first_or_create(discord_id=member.id)
        secondUser = User.first_or_create(discord_id=member.id)
 
        if( firstUser.money-number < 0 ):
            await interaction.response.send_message(f"Have no enough money.")
            return

        firstUser.money -= number
        firstUser.save()
        
        secondUser.money += number
        secondUser.save()
        
        await interaction.response.send_message(f"Transfered = {number}")
