from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
# Создаем объект FastAPI
app = FastAPI()

# Инициализация словаря users
users = {
    '1': 'Имя: Example, возраст: 18'
}

# GET запрос по маршруту '/users'
@app.get('/')
async def get_users():
    return users

# POST запрос по маршруту '/user/{username}/{age}'
@app.post('/user/{username}/{age}')
async def add_user(
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20)],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120)]
):
    # Находим максимальный ключ
    max_id = max(map(int, users.keys())) if users else 0
    new_id = str(max_id + 1)
    users[new_id] = f'Имя: {username}, возраст: {age}'
    return f"User {new_id} is registered"

# PUT запрос по маршруту '/user/{user_id}/{username}/{age}'
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
    user_id: Annotated[int, Path(description='Enter User ID', ge=1)],
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20)],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120)]
):
    if str(user_id) not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[str(user_id)] = f'Имя: {username}, возраст: {age}'
    return f"User {user_id} has been updated"

# DELETE запрос по маршруту '/user/{user_id}'
@app.delete('/user/{user_id}')
async def delete_user(
    user_id: Annotated[int, Path(description='Enter User ID', ge=1)]
):
    if str(user_id) not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[str(user_id)]
    return f"User {user_id} has been deleted"
