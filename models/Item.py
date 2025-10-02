# Created with magi tool
from orator import DatabaseManager, Model

class Item(Model):
    __fillable__ = [
        'id',
        'created_at',
        'updated_at',
        'icon',
        'name',
        'description',
        'script'
    ]
    