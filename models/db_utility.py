import pymongo


def auth_db(db, db_config):
    if db_config['username'] is not None and db_config['password'] is not None:
        db.authenticate(db_config['username'], db_config['password'])