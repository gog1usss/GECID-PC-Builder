from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from db import get_db_cursor
from values import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

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
            raise HTTPException(status_code=404,detail='User with this name already exists')
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

    await cur.execute('select id, password_hsd from users where username = %s', (form_data.username,))
    user_db = await cur.fetchone()

    if not user_db or not verify_password(form_data.password, user_db['password_hsd']):
        raise HTTPException(
            status_code=401,
            detail= 'Invalid login or password',
            headers= {"WWW-Authenticate": "Bearer"}
        )

    token = create_acc_token(data={"sub": str(user_db['id'])})
    return {
        'access_token': token,
        'token_type' : 'bearer'
    }
async def get_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="failed to check info",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except jwt.PyJWTError:
        raise credentials_exception



