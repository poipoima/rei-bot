# Created with magi tool
from orator import DatabaseManager, Model
from models.Item import Item

class Inventory(Model):
    __fillable__ = [
        'id',
        'created_at',
        'updated_at',
        'user_id',
        'item_id',
        'amount'
    ]
    
    def getItem(self):
        return Item.where( "id", self.item_id ).first()