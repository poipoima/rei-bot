from models.User import User
import math

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = [
            "Leaf",
            "Stone",
            "Iron",
            "Tungsten",
            "Titanium",
            "Well Known",
            "Segfault",
            "ㅤ",
            "Ultimate",
            "God Tier",
        ]

    @app_commands.command(name="level", description="Check your level.")
    async def level(self, interaction: discord.Interaction):
        localUser = User.first_or_create(discord_id=interaction.user.id)
        localUser = User.first_or_create(discord_id=interaction.user.id)

        embed = discord.Embed(
            title=interaction.user.display_name,
            description=f"""Your level is {localUser.level}
            Messages: {localUser.msgs}""",
            color=discord.Color.yellow()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        localUser = User.first_or_create(discord_id=message.author.id)
        localUser = User.first_or_create(discord_id=message.author.id)

        localUser.msgs += 1
        localUser.save()

        if( localUser.msgs < 3 ):
            role = discord.utils.get(message.guild.roles, name=self.roles[0])
            await message.author.add_roles(role)


        if localUser.msgs % 50 == 0:
            localUser.level += 1
            localUser.save()

            embed = discord.Embed(
                title=message.author.display_name,
                description=f"""🎉 Reach a new **level {localUser.level}**!""",
                color=discord.Color.yellow()
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)

            await message.reply(embed=embed)
        

        if( localUser.level % 20 == 0):
            idx = min(localUser.level // 20, len(self.roles) - 1)

            role = discord.utils.get(message.guild.roles, name=self.roles[ idx ])
            if role:
                await message.author.add_roles(role)

