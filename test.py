from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional
from database import get_db_cursor

SECRET_KEY = "my_super_secret_key_gecid"  # В реальных проектах это прячут в .env файл
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Токен "живет" 1 час

# Настройка для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Эта штука говорит FastAPI, где находится эндпоинт для получения токена (для кнопки Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['АВТОРИЗАЦИЯ']
)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# --- НОВАЯ СХЕМА ДЛЯ ОБНОВЛЕНИЯ ПРОФИЛЯ ---
class UserUpdate(BaseModel):
    new_username: Optional[str] = None
    new_password: Optional[str] = None


def get_password_hash(password: str):
    """Превращает обычный пароль в нечитабельный хэш. Обрезаем до 72 символов для bcrypt."""
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str):
    """Проверяет, совпадает ли введенный пароль с хэшем из базы"""
    return pwd_context.verify(plain_password[:72], hashed_password)


def create_access_token(data: dict):
    """Генерирует JWT токен"""
    to_encode = data.copy()
    # Исправлена синтаксическая ошибка: добавлена 'S' в конце и закрывающая скобка ')'
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/register')
async def register_user(user: UserCreate, cur=Depends(get_db_cursor)):
    """Регистрация нового пользователя"""
    try:
        # Проверяем, не занято ли имя
        await cur.execute("SELECT id FROM users WHERE username = %s", (user.username,))
        if await cur.fetchone():
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

        # Хэшируем пароль и сохраняем в базу
        hashed_password = get_password_hash(user.password)
        query = "INSERT INTO users (username, email, password_hsd) VALUES (%s, %s, %s)"
        await cur.execute(query, (user.username, user.email, hashed_password))

        return {"status": "success", "message": "Пользователь успешно зарегистрирован!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), cur=Depends(get_db_cursor)):
    """Вход по логину и паролю. Выдает JWT токен."""

    # 1. Ищем пользователя по username (ИЗМЕНЕНИЕ: Достаем token_version)
    await cur.execute("SELECT id, password_hsd, token_version FROM users WHERE username = %s", (form_data.username,))
    user_db = await cur.fetchone()

    # 2. Проверяем существование юзера и совпадение пароля
    if not user_db or not verify_password(form_data.password, user_db['password_hsd']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Если всё ок - создаем токен.
    # ИЗМЕНЕНИЕ: Теперь зашиваем внутрь токена не только ID, но и текущую ВЕРСИЮ токена!
    access_token = create_access_token(data={
        "sub": str(user_db['id']),
        "version": user_db.get('token_version', 1)
    })

    # ВАЖНО: FastAPI требует возвращать именно в таком формате!
    return {"access_token": access_token, "token_type": "bearer"}


# --- НОВЫЙ ЭНДПОИНТ: ВЫХОД ИЗ СИСТЕМЫ ---
@router.post('/logout')
async def logout(token: str = Depends(oauth2_scheme), cur=Depends(get_db_cursor)):
    """Выход из системы (добавление токена в черный список)"""
    try:
        await cur.execute("INSERT IGNORE INTO token_blacklist (token) VALUES (%s)", (token,))
        return {"status": "success", "message": "Вы успешно вышли из системы. Токен аннулирован."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- НОВЫЙ ЭНДПОИНТ: ОБНОВЛЕНИЕ ПРОФИЛЯ ---
@router.patch('/profile')
async def update_profile(
        update_data: UserUpdate,
        token: str = Depends(oauth2_scheme),
        cur=Depends(get_db_cursor),
        user_id: int = Depends(get_current_user)
):
    """Обновление профиля пользователя"""
    try:
        # 1. Меняем имя пользователя
        if update_data.new_username:
            # Проверяем, не занято ли новое имя
            await cur.execute("SELECT id FROM users WHERE username = %s", (update_data.new_username,))
            if await cur.fetchone():
                raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
            await cur.execute("UPDATE users SET username = %s WHERE id = %s", (update_data.new_username, user_id))

        # 2. Меняем пароль
        if update_data.new_password:
            hashed_pw = get_password_hash(update_data.new_password)

            # ИЗМЕНЕНИЕ: Обновляем пароль И увеличиваем версию токенов на +1!
            # Это мгновенно "убьет" ВСЕ старые токены на всех устройствах злоумышленника.
            await cur.execute(
                "UPDATE users SET password_hsd = %s, token_version = token_version + 1 WHERE id = %s",
                (hashed_pw, user_id)
            )

            return {"status": "success",
                    "message": "Пароль изменен. Выполнен выход со всех устройств. Авторизуйтесь заново."}

        return {"status": "success", "message": "Профиль успешно обновлен!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ОБНОВЛЕННЫЙ ОХРАННИК: ТЕПЕРЬ ПРОВЕРЯЕТ BLACKLIST И ВЕРСИЮ ТОКЕНА ---
async def get_current_user(token: str = Depends(oauth2_scheme), cur=Depends(get_db_cursor)):
    """
    Эта функция вешается на другие эндпоинты.
    Она расшифровывает токен и возвращает ID текущего пользователя.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # --- ПРОВЕРКА BLACKLIST (для одиночного выхода через /logout) ---
        await cur.execute("SELECT id FROM token_blacklist WHERE token = %s", (token,))
        if await cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен отозван (выполнен выход)"
            )

        # Расшифровываем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_version: int = payload.get("version")  # ИЗМЕНЕНИЕ: Достаем версию из токена

        if user_id is None or token_version is None:
            raise credentials_exception

        # --- ПРОВЕРКА ВЕРСИИ УЧЕТНЫХ ДАННЫХ ---
        # Запрашиваем актуальную версию из базы
        await cur.execute("SELECT token_version FROM users WHERE id = %s", (int(user_id),))
        user_db = await cur.fetchone()

        # Если юзера удалили или версия в базе не совпадает с версией в токене (пароль меняли)
        if not user_db or user_db.get('token_version', 1) != token_version:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Сессия устарела (пароль был изменен). Пожалуйста, авторизуйтесь заново."
            )

        return int(user_id)  # Возвращаем ID пользователя!
    except jwt.PyJWTError:
        raise credentials_exception
