from fastapi import APIRouter, status, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
import bcrypt
from routes.resumeRoute import conn
import traceback
import binascii
from jose import jwt , JWTError
from decouple import config

from datetime import timedelta, datetime

jwt_secret_key = config("JWT_SECRET_KEY")
jwt_alogorithm = config("JWT_ALGORITHM")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)




bcrypt_context= CryptContext(schemes=['bcrypt'],deprecated='auto')

salt = bcrypt.gensalt()



def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode = {'sub':username,'id':user_id}
    expires_delta = datetime.utcnow() + expires_delta
    encode.update({'exp':expires_delta})
    return jwt.encode(encode,jwt_secret_key,algorithm=jwt_alogorithm)


@router.post("/decode_jwt", status_code=status.HTTP_201_CREATED)
async def get_current_user(token:str):
    try:
        payload = jwt.decode(token,jwt_secret_key,algorithms=[jwt_alogorithm])
        username = payload.get('sub')
        user_id = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
        return {'username':username,'id':user_id}
    except JWTError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')













class CreateUserData(BaseModel):
    email:str
    password:str

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_data: CreateUserData):
    # hashed_password = bcrypt_context.hash(create_user_data.password)
    try:
        hashed_password = bcrypt.hashpw(create_user_data.password.encode(), salt)   
        cursor = conn.cursor()
        query = """
            INSERT INTO public."User" ("UserName", "Email", "Password", "RoleId", "Status")
            VALUES (%s, %s, %s, %s,%s)
            RETURNING "UserId";
        """
        values = (
            'armss',
            create_user_data.email,
            hashed_password,
            1,
            True
        )
        cursor.execute(query, values)
        conn.commit()
        
        # Fetch the generated UserId
        user_id = cursor.fetchone()[0]
        print(f"User inserted with UserId: {user_id}")
        return user_id
    except Exception as e:
        traceback.print_exc()
        conn.rollback()
        print(f"Error inserting user: {e}")
        return None
    finally:
        cursor.close()

   


@router.post("/token")
async def UserLogin(user_data:CreateUserData):

    try:
        cursor = conn.cursor()
        query = """SELECT "UserId","Email", "Password" FROM "User" WHERE "User"."Email" = %s;"""
        cursor.execute(query, (user_data.email,))
        user_table_info = cursor.fetchone()
        print(user_data)

        if not user_table_info:
            print("user doesn't exists")
            return False
        if bcrypt.checkpw(user_data.password.encode(),binascii.unhexlify(user_table_info[2][2:])): 
            print("USER EXISTS")
            token = create_access_token(user_table_info[1], user_table_info[0],timedelta(minutes=60))
        else:
            print("Password is incorrect")
            return "Password is Incorrect"

        print(user_table_info)
        return f"Successfull Authentication. JWT TOKEN is {token}"
    except Exception as e:
        traceback.print_exc()
        conn.rollback()
        print(f"Error fetching user credentials: {e}")
        return None
    finally:
        cursor.close()


