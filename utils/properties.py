from .envs import get_property

DATABASE_URL = get_property('db.url')
DATABASE_USER = get_property('db.user','')
DATABASE_PASS = get_property('db.pass','')