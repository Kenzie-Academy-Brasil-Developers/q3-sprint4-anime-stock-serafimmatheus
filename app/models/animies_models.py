from psycopg2 import sql
from app.models import ConectionBD


class Animes(ConectionBD):
    def __init__(self, **kwargs):
        self.anime = kwargs["anime"]
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]


    @staticmethod
    def check_keys():
        keys_validate = ["anime", "released_date", "seasons"]

    @classmethod
    def create_anime(cls, data: dict):
        cls.openConection()

        cls.cur.execute(
            """
                create table if not exists animes(
                    id 				BIGSERIAL PRIMARY key,
                    anime 			VARCHAR(100) NOT NULL unique,
                    released_date 	DATE NOT null,
                    seasons 		INTEGER NOT NULL
                );
            """
        )

        query = """
            INSERT INTO animes
                ("anime", "released_date", "seasons")
            VALUES
                (%s, %s, %s)
            RETURNING 
                *;
        """

        values = (data['anime'].title(), data['released_date'], data['seasons'])
        
        cls.cur.execute(query, values)

        result = cls.cur.fetchone()

        cls.closeConection(commit=False)

        return result


    @classmethod
    def get_animes(cls):
        cls.openConection()

        query = """
            SELECT 
                *
            FROM
                animes
            ORDER BY
                id;
        """

        cls.cur.execute(query)

        results = cls.cur.fetchall()

        cls.closeConection()

        return results


    @classmethod
    def get_animes_by_id(cls, id):
        cls.openConection()

        query = sql.SQL("""
            SELECT
                *
            FROM
                animes
            WHERE
                id = {id}
        """).format(
            id = sql.Literal(id)
        )

        cls.cur.execute(query)

        result = cls.cur.fetchone()

        cls.closeConection()

        return result


    @classmethod
    def update_animes(cls, data, id):
        cls.openConection()

        # key = [i for i in data.keys()]
        # value = [i for i in data.values()]
        # if len(key) >=1 and "anime" in str(key):
        #     data_1 = dict(zip(key, value))
        #     data_1["anime"] = data_1["anime"].title()
        #     keys = [sql.Identifier(key) for key in data_1.keys()]
        #     values = [sql.Literal(value) for value in data_1.values()]

        # elif len(key) == 1 and "anime" in str(key):
        #     data_1 = dict(zip(key, value))
        #     data_1["anime"] = data_1["anime"].title()
        #     keys = [sql.Identifier(key) for key in data_1.keys()]
        #     values = [sql.Literal(value) for value in data_1.values()]
        # else:
        #     keys = [sql.Identifier(key) for key in data.keys()]
        #     values = [sql.Literal(value) for value in data.values()]


        if data.get("anime"):
            data["anime"] = data["anime"].title()
        
        keys = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]
        


        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({keys}) = row ({values})
                WHERE
                    id = {id}
                RETURNING
                    *;
            """
        ).format(
            keys = sql.SQL(",").join(keys),
            values = sql.SQL(",").join(values),
            id = sql.Literal(id)
        )

        cls.cur.execute(query)

        result_update = cls.cur.fetchone()

        cls.closeConection(commit=False)

        return result_update

    @classmethod
    def deleted_animes(cls, id):
        cls.openConection()

        query = sql.SQL("""
            DELETE FROM
                animes
            WHERE
                id = {id}
            RETURNING 
                *
        """).format(
            id = sql.Literal(id)
        )

        cls.cur.execute(query)

        deleted = cls.cur.fetchone()

        cls.closeConection(commit=False)
        return deleted
        