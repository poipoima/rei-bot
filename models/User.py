from orator import DatabaseManager, Model
from models.Inventory import Inventory

class User(Model):
    __fillable__ = [
        'id',
        'discord_id',
        'money',
        'shards',
        'level',
        'msgs',
        'role',
        'created_at',
        'updated_at'
    ]

    def getInventory(self):
        return Inventory.where( "user_id", self.id ).get()