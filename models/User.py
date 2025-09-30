from orator import DatabaseManager, Model

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
 