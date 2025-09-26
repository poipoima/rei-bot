from models.User import User

class Eloquent(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @app_commands.command(name="test", description="Check the eloquent.")
    async def test(self, interaction: discord.Interaction):
        localUser = User.first_or_create(discord_id=interaction.user.id)

        await interaction.response.send_message(f"Your DB index = {localUser.id}")
    