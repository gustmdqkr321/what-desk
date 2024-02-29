from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.staticfiles import StaticFiles
from typing import List

import os
import shutil
import uuid
import base64
import json

from detect import detect
from process_image import process
from sqlalchemy.orm import Session
from database import crud
from database.models import *
from database.schemas import *
from database.database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

SECRET_KEY = "secret"  # temp
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/uploaded_images",
          StaticFiles(directory="uploaded_images"), name="uploaded_images")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password: str):
    return pwd_context.hash(password)


async def authenticate_user(db: Session, user: User):
    user_db = await crud.read_user(db, user.user_id)
    if not user_db:
        return False
    if not verify_password(user.password, user_db.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_payload(token):
    header, payload, signature = token.split(".")

    decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
    parsed_payload = json.loads(decoded_payload)

    return parsed_payload


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_payload(token)
    try:
        validation = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

# 메인


@app.get("/")
async def root():
    return "hello world"


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*" 사용
    allow_headers=["*"],  # 모든 헤더를 허용하려면 "*" 사용
)
result_folder = "/Users/park_sh/Desktop/what-desk/back/result"
upload_folder = "/Users/park_sh/Desktop/what-desk/back/uploads"


@app.get("/get_image/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join(result_folder, image_filename)
    return FileResponse(image_path, media_type="image/jpeg")


# 이미지 업로드 및 처리 결과 반환
@app.post("/process_image/")
async def process_image(file: UploadFile):
    return process(file)


@app.post("/user/sign_up", response_model=HashedUser)
async def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(user.password)
    user = HashedUser(**user.model_dump(), hashed_password=hashed_password)

    user_db = await crud.read_user(db, user.user_id)
    if user_db:
        raise HTTPException(status_code=409, detail="User ID already exists")

    await crud.create_user(db, user)
    return {"message": "User deleted successfully"}


@app.post("/token")
async def generate_token(user: User, db: Session = Depends(get_db)):
    user = await authenticate_user(db, user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "iss": "what-desk",
        "sub": user.user_id
    }
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=data, expires_delta=access_token_expires
    )
    return {
        "user_id": user.user_id,
        "token": Token(access_token=access_token, token_type="bearer")
    }


@app.get("/user/me")
async def current_user(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}


@app.post("/post/create")
async def create_post(post: PostForm, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    await crud.create_post(db, post, user_id)
    return {"message": "Post created successfully"}


@app.get("/post/search", response_model=List[PostPreview])
async def search_posts(
    category: str | None = None,
    author_id: str | None = None,
    keyword: str | None = None,
    db: Session = Depends(get_db),
):
    posts = await crud.search_posts(
        db, author_id=author_id, category=category, keyword=keyword
    )
    return posts


@app.get("/post/{post_id}", response_model=Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = await crud.increment_view_count(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post does not exist.")
    return post
    

@app.delete("/post/{post_id}")
async def delete_post(post_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    post = await crud.read_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied: You are not the author of this post")
    
    await crud.delete_post(db, post)
    return {"message": "Post deleted successfully"}


@app.post("/post/like/{post_id}")
async def like_post(post_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    post = await crud.read_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await crud.create_like(db, user_id, post_id)
    return {"message": "User liked post successfully"}


@app.post("/comment/create")
async def create_comment(comment: CommentForm, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    post = await crud.read_post(db, comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud.create_comment(db, comment, user_id)
    return {"messaeg": "Comment created successfully"}


@app.get("/comment/search", response_model=List[Comment])
async def search_comment(
    post_id: str | None = None,
    author_id: str | None = None,
    db: Session = Depends(get_db),
):
    comments = await crud.read_comment(
        db, author_id=author_id, post_id=post_id
    )
    return comments


@app.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    comment = await crud.read_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied: You are not the author of this comment")
    
    await crud.delete_comment(db, comment)
    return {"message": "Comment deleted successfully"}


@app.post("/image/upload", response_model=Image)
async def upload_image(file: UploadFile, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    os.makedirs("uploaded_images", exist_ok=True)

    filename = file.filename
    file_extension = os.path.splitext(filename)[1]
    image_id = str(uuid.uuid4()) + file_extension

    with open(f"uploaded_images/{image_id}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Image(image_id=image_id, filename=filename)
    return await crud.created_image(db, image)


# test
# 서버 오픈 ->  uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 가상환경 -> source venv/bin/activate, 종료 -> deactivate
# db -> db 실행(brew services start postgresql), db 확인(psql -U admin -d mydb), db 종료(brew services stop postgresql), SELECT * FROM users;
# http://210.178.142.51:????
