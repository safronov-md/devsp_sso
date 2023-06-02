from exceptions import ProblemBadRequest, ProblemUnauthorized
from fastapi import HTTPException
from .auth import Auth
from .models import UserUpdateRequestModel
import devsp_db

auth_handler = Auth()


def register_user(user_model: UserUpdateRequestModel):
    user = devsp_db.get_from_db("users", [f"email=eq.{user_model.email}"])
    if len(user) != 0:
        raise HTTPException(
            status_code=409, detail='Email user already exist.')
    hashed_password = auth_handler.encode_password(user_model.password)
    data = user_model.dict()
    data["password"] = hashed_password
    result = devsp_db.post_data_to_db("users", data)
    if not result:
        raise ProblemBadRequest("Something went wrong!")
    user = devsp_db.get_from_db("users", [f"email=eq.{user_model.email}"])
    return user[0]


def signin_user(email, password):
    user = devsp_db.get_from_db("users", [f"email=eq.{email}"])
    if len(user) == 0:
        raise ProblemUnauthorized("Provided email is invalid")
    if not auth_handler.verify_password(password, user[0]['password']):
        raise ProblemUnauthorized("Provided password is invalid")
    return user[0]


def update_user(user_model: UserUpdateRequestModel):
    user = get_user_by_email(user_model.email)
    if not user:
        raise ProblemBadRequest(f"User with provided email = {user_model.email} wasn't found")
    hashed_password = auth_handler.encode_password(user_model.password)
    upd_data = user_model.dict()
    upd_data["id"] = user[0]['id']
    upd_data["password"] = hashed_password
    put_request = devsp_db.put_data_to_db(f"users?id=eq.{user[0]['id']}", upd_data)
    if not put_request:
        raise ProblemBadRequest("Something went wrong!")
    user = get_user_by_email(user_model.email)
    return user[0]


def get_all_users():
    user = devsp_db.get_from_db("users", [])
    return user


def get_user_by_email(email: str):
    user = devsp_db.get_from_db("users", [f"email=eq.{email}"])
    return user


def get_user_by_id(id: int):
    user = devsp_db.get_from_db("users", [f"id=eq.{id}"])
    return user
