from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()


# Base de datos simulada en memoria
fake_users_db = {"1": {"name": "Alice", "age": 25}, "2": {"name": "Bob", "age": 30}}


# Modelo de datos para Usuario
class User(BaseModel):
    name: str
    age: int


# Configuración de autenticación con token simulado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token: str):
    if token == "fake-token":
        return {"sub": "user"}
    raise HTTPException(status_code=401, detail="Invalid token")


# Endpoints


@app.get("/users", response_model=List[User])
def get_users():
    """Devuelve la lista de usuarios."""
    return list(fake_users_db.values())


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    """Obtiene un usuario por su ID."""
    if user_id in fake_users_db:
        return fake_users_db[user_id]
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users", response_model=User)
def create_user(user: User):
    """Crea un nuevo usuario."""
    user_id = str(len(fake_users_db) + 1)
    fake_users_db[user_id] = user.dict()
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    """Elimina un usuario por su ID."""
    if user_id in fake_users_db:
        del fake_users_db[user_id]
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """Permite subir un archivo y retorna sus metadatos."""
    return {"filename": file.filename, "content_type": file.content_type}


@app.get("/secure-data")
def get_secure_data(token: str = Depends(oauth2_scheme)):
    """Ruta protegida que requiere autenticación por token."""
    token_data = fake_decode_token(token)
    return {"message": "This is a protected route", "token_data": token_data}
