import psycopg2
from os import getenv



class ConectionBD:
    configs = {
        "host": getenv("DATA_HOST"),
        "user": getenv("DATA_USER"),
        "database": getenv("DATA_BASE"),
        "password": getenv("DATA_PASSWORD"),
    }

    @classmethod
    def openConection(cls):
        cls.conn = psycopg2.connect(**cls.configs)
        cls.cur = cls.conn.cursor()


    @classmethod
    def closeConection(cls, commit=True):
        if not commit:
            cls.conn.commit()
            
        cls.cur.close()
        cls.conn.close()

    @classmethod
    def serialized_animes(cls, data: dict, lista=False):
        keys = ["id", "anime", "released_date", "seasons"]
        
        if lista:
            result = [dict(zip(keys, anime))for anime in data]
            return result

        return dict(zip(keys, data))
