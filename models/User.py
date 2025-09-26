from orator import DatabaseManager, Model

class User(Model):
    __fillable__ = ['id', 'discord_id', 'created_at', 'updated_at']
 