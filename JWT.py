from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from db import get_db_cursor
from values import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/pass/login")

router = APIRouter(
    prefix='/api/v1/pass',
    tags=['PASS-hash-auth']
)

class User_Create(BaseModel):
    username: str
    email: str
    password: str

class User_Update(BaseModel):
    updated_username: Optional[str] = None
    updated_password: Optional[str] = None

def get_pass_hash(password):
    return pwd_context.hash(password[:72])

def verify_password(p_password,hashed_password):
    return pwd_context.verify(p_password[:72],hashed_password)

def create_acc_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/register')
async def register_user(user:User_Create, cur = Depends(get_db_cursor)):

    try:
        await cur.execute('select id from users where username = %s', (user.username,))
        if await cur.fetchone():
            raise HTTPException(status_code=400,detail='User with this name already exists')
        hashed_pass = get_pass_hash(user.password)
        query = 'insert into users (username,email, password_hsd) Values(%s, %s, %s)'

        await cur.execute(query,(user.username,user.email,hashed_pass))

        return {"status": "success", "message": "The registration successes"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), cur = Depends(get_db_cursor)):

    await cur.execute('select id, password_hsd, token_version from users where username = %s', (form_data.username,))
    user_db = await cur.fetchone()

    if not user_db or not verify_password(form_data.password, user_db['password_hsd']):
        raise HTTPException(
            status_code=401,
            detail= 'Invalid login or password',
            headers= {"WWW-Authenticate": "Bearer"}
        )

    token = create_acc_token(data={
        'sub': str(user_db['id']),
        'version': user_db.get('token_version',1)
        })
    return {
        'access_token': token,
        'token_type' : 'bearer'
    }
@router.post('/logout')
async def logout (token: str = Depends(oauth2_scheme), cur = Depends(get_db_cursor)):
    try:
        await cur.execute ('INSERT IGNORE INTO token_blacklist (token) VALUES (%s)', (token,))
        return {'status': 'success', 'message': 'You successfully left your account'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_user(token: str = Depends(oauth2_scheme), cur = Depends(get_db_cursor)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to check info",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        await cur.execute('Select id from token_blacklist Where token = %s', (token,))
        if await cur.fetchone():
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= 'Token returned (Unauthorized)'
            )
        payload = jwt.decode(token,SECRET_KEY, algorithms= [ALGORITHM])
        user_id: str = payload.get('sub')
        token_version: int = payload.get('version')

        if user_id is None or token_version is None:
            raise credentials_exception

        await cur.execute('select token_version from users where id = %s', (int(user_id),))
        user_db = await cur.fetchone()

        if not user_db or user_db.get('token_version',1) != token_version:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Session expired. Please Log IN'
            )

        return int(user_id)

    except jwt.PyJWTError:
        raise credentials_exception

@router.patch('/profile')
async def update_profile(
        update_data: User_Update,
        token: str = Depends(oauth2_scheme),
        cur = Depends(get_db_cursor),
        user_id: int = Depends(get_user)
):
    try:
        if update_data.updated_username:
            await cur.execute('Select id from users Where username = %s', (update_data.updated_username,))
            if await cur.fetchone():
                raise HTTPException(status_code=400, detail='User with this name already exists')
            await cur.execute('Update users SET username = %s Where id = %s',(update_data.updated_username,user_id))

        if update_data.updated_password:
            hashed_pw = get_pass_hash(update_data.updated_password)

            await cur.execute(
                'Update users Set password_hsd = %s, token_version = token_version +1 Where id = %s',
                (hashed_pw, user_id)
            )
            return {
                'status': 'success',
                'message': 'Password has been successfully changed'
            }
        return {
            'status': 'success',
            'message': 'Profile has been successfully changed'
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
