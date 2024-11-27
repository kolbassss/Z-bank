from fastapi import APIRouter, HTTPException
from db_users import session, User
from sqlalchemy import select
import bcrypt

managment_user = APIRouter()

@managment_user.post("/create_user")
def register_user(name:str, surname:str, email:str, number:str, password:str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=name, surname=surname, email=email, number=number, password=hashed_password)
    session.add(new_user)
    session.commit()
    return {"message": "user registered"}

@managment_user.post("/auth_user")
def auth_user(email:str, password:str):
    global profile
    profile_user = session.scalars(select(User).where(User.email==email))
    try:
        profile = profile_user.all()[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="not found")
    if bcrypt.hashpw(password.encode('utf-8'), profile.password) == profile.password:
        profile.authorize = "authorize"
        return {"message": "authorized successfully"}
    raise HTTPException(status_code=404, detail="check enter data")

@managment_user.get("/read_profile_user")
def read_profile_user():
    if profile == None or profile.authorize == "not authorize":
        raise HTTPException(status_code=401, detail="you not authrize")
    return profile

@managment_user.put("/update_name_profile")
def update_name_profile_user(new_name:str):
    if profile.authorize == "authorize":
        profile.name = new_name
        session.commit()
        return {"message": "name update"}
    raise HTTPException(status_code=401, detail="you not authrize")
    
@managment_user.put("/update_surname_profile")
def update_surname_profile_user(new_surname:str):
    if profile.authorize == "authorize":
        profile.surname = new_surname
        session.commit()
        return {"message": "surname update"}
    raise HTTPException(status_code=401, detail="you not authrize")
    
@managment_user.put("/update_password_profile")
def update_password_profile_user(current_password:str, new_password:str, confirm_new_password:str):
    if profile.authorize == "authorize":
        if bcrypt.hashpw(current_password.encode('utf-8'), profile.password) == profile.password:
            if new_password == confirm_new_password:
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                profile.password = hashed_new_password
                session.commit()
                return {"message": "password update"}
            raise HTTPException(status_code=400, detail="invalid confirm password")
        raise HTTPException(status_code=400, detail="invalid password")
    raise HTTPException(status_code=401, detail="you not authrize")

@managment_user.delete("/delete_profile_user")
def delete_user_profile(you_really_delete_your_profile:str):
    if profile.authorize == "authorize":
        if you_really_delete_your_profile == 'Yes':
            session.delete(profile)
            session.commit
            return {"message": "your profile delete"}
        elif you_really_delete_your_profile == 'No':
            return {""}
        raise HTTPException(status_code=400, detail="invalid request")
    raise HTTPException(status_code=401, detail="you not authrize")
