# Created with magi tool
from models.User import User
from models.Inventory import Inventory as InventoryObject

class Inventory(commands.GroupCog, name="inventory", description="inventory commands"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="list", description="list of items")
    async def list(self, interaction: discord.Interaction):
        localUser = User.first_or_create(discord_id=interaction.user.id)
        localUser = User.first_or_create(discord_id=interaction.user.id)

        allItems = []
        inventoryItems = localUser.getInventory()

        for inventoryItem in inventoryItems:
            Item = inventoryItem.getItem()
            allItems.append(f"{Item.icon} {Item.name} - {inventoryItem.amount}")

        embed = discord.Embed(
            title="Inventory",
            description= "\n".join(allItems),
            color=discord.Color.green() 
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)
        
    async def transfer_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ):
        localUser = User.first_or_create(discord_id=interaction.user.id)
        localUser = User.first_or_create(discord_id=interaction.user.id)

        inventoryItems = localUser.getInventory()

        choices = []
        for inventoryItem in inventoryItems:
            Item = inventoryItem.getItem()
            if current.lower() in Item.name.lower():
                choices.append(app_commands.Choice(
                    name=f"{Item.icon} {Item.name} ({inventoryItem.amount})",
                    value=str(Item.id)
                ))

        return choices[:25]

    @app_commands.command(name="transfer", description="transfer items")
    @app_commands.describe(member="Who to transfer to", item="Which item", number="How many")
    async def transfer(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        item: str,
        number: int
    ):
        localUser = User.first_or_create(discord_id=interaction.user.id)
        localUser = User.first_or_create(discord_id=interaction.user.id)

        secondUser = User.first_or_create(discord_id=member.id)
        secondUser = User.first_or_create(discord_id=member.id)

        inventoryItems = localUser.getInventory()

        chosenItem = None
        for inventoryItem in inventoryItems:
            Item = inventoryItem.getItem()
            if str(Item.id) == item:
                chosenItem = (Item, inventoryItem)
                break

        if not chosenItem:
            return await interaction.response.send_message("❌ Item not found in your inventory.", ephemeral=True)

        Item, inventoryItem = chosenItem

        if inventoryItem.amount < number:
            return await interaction.response.send_message(
                f"❌ You don’t have enough {Item.name}. You only have {inventoryItem.amount}.",
                ephemeral=True
            )

        inventoryItem.amount -= number
        inventoryItem.save()

        NewUserInventory = InventoryObject.first_or_create(user_id=secondUser.id, item_id=inventoryItem.item_id)
        NewUserInventory = InventoryObject.first_or_create(user_id=secondUser.id, item_id=inventoryItem.item_id)
        NewUserInventory.amount = ( number if NewUserInventory.amount is None else NewUserInventory.amount + number ) 
        NewUserInventory.save()
        
        if( inventoryItem.amount < 1 ):
            inventoryItem.delete()

        await interaction.response.send_message(
            f"✅ Transferred {number}x {Item.icon} {Item.name} to {member.mention}"
        )

    transfer.autocomplete("item")(transfer_autocomplete)