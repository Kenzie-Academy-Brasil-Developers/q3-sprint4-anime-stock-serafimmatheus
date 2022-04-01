from http import HTTPStatus
from app.models.animies_models import Animes
from flask import jsonify, request
from psycopg2.errors import UndefinedColumn
from psycopg2.errors import UniqueViolation
from psycopg2.errors import UndefinedTable


def create():
    data = request.get_json()
    try:
        new_data = Animes(**data)
        result = Animes.create_anime(new_data.__dict__)
    except UniqueViolation:
        return {"error": "anime is already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except KeyError as e:
        return {"required_keys": ["anime", "released_date", "seasons"], "missing_keys": e.args}, HTTPStatus.UNPROCESSABLE_ENTITY
    
    new_result = Animes.serialized_animes(result)

    return new_result, HTTPStatus.CREATED


def get_all_animes():

    try:
        result = Animes.get_animes()
        data = Animes.serialized_animes(result, lista=True)
    except UndefinedTable:
        return jsonify([]), HTTPStatus.OK

    return {"data": data}, HTTPStatus.OK


def get_one_by_id_anime(id):

    try:
        data = Animes.get_animes_by_id(id)
        result = Animes.serialized_animes(data)
    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    return {"data": [result]}, HTTPStatus.OK


def update(id):
    get = request.get_json()
    try:
        data = Animes.update_animes(get, id)
        data_serialized = Animes.serialized_animes(data)
    except UniqueViolation:
        return {"error": "anime is already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except UndefinedColumn as e:
        text = str(e.args).split('"')[1]
        return {"available_keys": ["anime", "released_date", "seasons"], "wrong_keys_sended": [f"{text}"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    except (UndefinedTable, TypeError):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except KeyError as e:
        text = str(e.args).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        return {"available_keys": ["anime", "released_date", "seasons"], "wrong_keys_sended": [f"{text}"]}, HTTPStatus.UNPROCESSABLE_ENTITY

    

    return data_serialized, HTTPStatus.OK


def delete(id):
    try:
        deleted = Animes.deleted_animes(id)
        if not deleted:
            return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except UndefinedTable:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT
    
    


    