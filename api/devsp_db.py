import os
import jwt
import requests

from exceptions import ProblemBadRequest

db_secret = os.getenv("DEVSP_DB_SECRET")
payload = {"role": os.getenv("DEVSP_DB_ROLE")}
token = jwt.encode(payload, db_secret, algorithm='HS256')


def get_from_db(table: str, fields: list) -> dict:
    r = f"http://postgrest:3000/{table}?"
    for field in fields:
        r = f"{r}{field}&"
    r = requests.get(r, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        return r.json()
    else:
        raise ProblemBadRequest(r.content)


def post_data_to_db(table: str, data: dict) -> bool:
    r = f"http://postgrest:3000/{table}"
    response = requests.post(r, headers={"Authorization": f"Bearer {token}"}, json=data)
    print(response.content)
    return True if response.status_code == 201 else False


def put_data_to_db(table: str, data: dict) -> bool:
    r = f"http://postgrest:3000/{table}"
    response = requests.put(r, headers={"Authorization": f"Bearer {token}"}, json=data)
    print(response.content)
    return True if response.status_code == 204 else False

