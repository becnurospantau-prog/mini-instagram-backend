from fastapi import FastAPI, Depends, HTTPException
from models import User

from sqlalchemy.orm import Session
from typing import List
import database, models, schemas, crud, auth
# main.py басында
from schemas import CommentUpdate
from schemas import RefreshTokenCreate

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Mini Instagram API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.username, user.email, user.password)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not auth.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth.create_access_token(username=db_user.username)
    return {"access_token": access_token, "token_type": "bearer"}

# =====================================================
# USERS CRUD
# =====================================================
@app.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db),
              current_user: str = Depends(auth.get_current_user)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int,
             db: Session = Depends(get_db),
             current_user: str = Depends(auth.get_current_user)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int,
                user: schemas.UserUpdate,
                db: Session = Depends(get_db),
                current_user: str = Depends(auth.get_current_user)):
    # Мынау дұрыс:
    updated = crud.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/users/{user_id}")
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_user: str = Depends(auth.get_current_user)):
    # Мынау да дұрыс:
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

# =====================================================
# POSTS CRUD
# =====================================================

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(auth.get_current_user)):  # User object, string емес
    return crud.create_post(
        db,
        current_user.id,   # int
        post.caption       # string
    )  

@app.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: str = Depends(auth.get_current_user)):
    return crud.get_posts(db)

@app.get("/posts/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int,
             db: Session = Depends(get_db),
             current_user: str = Depends(auth.get_current_user)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int,
                post: schemas.PostUpdate,
                db: Session = Depends(get_db),
                current_user: str = Depends(auth.get_current_user)):
    updated = crud.update_post(db, post_id, post)
    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated

@app.delete("/posts/{post_id}")
def delete_post(post_id: int,
                db: Session = Depends(get_db),
                current_user: str = Depends(auth.get_current_user)):
    success = crud.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}

# =====================================================
# MEDIA CRUD
# =====================================================
@app.get("/media", response_model=List[schemas.MediaOut])
def get_all_media(db: Session = Depends(get_db),
                  current_user: str = Depends(auth.get_current_user)):
    return crud.get_media(db)

@app.post("/media", response_model=schemas.MediaOut)
def create_media(media: schemas.MediaCreate,
                 db: Session = Depends(get_db),
                 current_user: str = Depends(auth.get_current_user)):
    return crud.create_media(db, media)

@app.get("/media/{media_id}", response_model=schemas.MediaOut)
def get_media_by_id(media_id: int,
                    db: Session = Depends(get_db),
                    current_user: str = Depends(auth.get_current_user)):
    media = crud.get_media_item(db, media_id)  # ← мұнда дұрыс атын қойдық
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

from fastapi import HTTPException

@app.put("/media/{media_id}", response_model=schemas.MediaOut)
def update_media(media_id: int, media_data: schemas.MediaCreate, db: Session = Depends(get_db)):
    media = crud.update_media(db, media_id, media_data)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media




@app.delete("/media/{media_id}")
def delete_media(media_id: int,
                 db: Session = Depends(get_db),
                 current_user: str = Depends(auth.get_current_user)):
    success = crud.delete_media(db, media_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"detail": "Media deleted"}


# =====================================================
# LIKES CRUD
# =====================================================
@app.post("/likes/{post_id}")
def toggle_like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    return crud.toggle_like(db, current_user.id, post_id)

@app.get("/likes/{post_id}")
def get_post_likes(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    return crud.get_likes(db, post_id)

@app.delete("/likes/{post_id}")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    success = crud.remove_like(db, current_user.id, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"status": "unliked", "post_id": post_id}

# =====================================================
# COMMENTS CRUD
# =====================================================

@app.post("/comments/")
def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db),
                current_user = Depends(auth.get_current_user)):
    db_comment = models.Comment(
        post_id=comment.post_id,
        author_id=current_user.id,
        text=comment.text
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/comments/{post_id}")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments
@app.get("/comments/")
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    return [{"id": c.id, "post_id": c.post_id, "author_id": c.author_id, "text": c.text, "created_at": c.created_at} for c in comments]


@app.put("/comments/{comment_id}")
def update_comment(comment_id: int, comment: CommentUpdate,
                   db: Session = Depends(get_db),
                   current_user = Depends(auth.get_current_user)):

    db_comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.author_id == current_user.id
    ).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found or not yours")

    # Егер text берілген болса ғана жаңарту
    if comment.text is not None:
        db_comment.text = comment.text

    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                   current_user = Depends(auth.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id,
                                              models.Comment.author_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not yours")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}

# =====================================================
# FOLLOWS CRUD
# =====================================================

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
import database, crud, auth

# =====================================================
# FOLLOWS CRUD
# =====================================================

@app.post("/follows/{user_id}")
def toggle_follow_user(user_id: int,
                       db: Session = Depends(database.get_db),
                       current_user: models.User = Depends(auth.get_current_user)):
    return crud.toggle_follow(db, current_user.id, user_id)

# Нақты unfollow
@app.delete("/follows/{user_id}")
def unfollow(user_id: int,
             db: Session = Depends(database.get_db),
             current_user: models.User = Depends(auth.get_current_user)):
    success = crud.unfollow_user(db, current_user.id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    return {"detail": "Unfollowed successfully"}

# Followers алу
@app.get("/follows/{user_id}/followers")
def followers(user_id: int,
              db: Session = Depends(database.get_db),
              current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_followers(db, user_id)

# Following алу
@app.get("/follows/{user_id}/following")
def following(user_id: int,
              db: Session = Depends(database.get_db),
              current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_following(db, user_id)




@app.post("/refresh_tokens/")
def create_refresh_token(token_data: RefreshTokenCreate, db: Session = Depends(get_db)):
    import uuid
    from datetime import datetime, timedelta

    jti = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=7)  # 7 күнге жарамды

    token = models.RefreshToken(
        user_id=token_data.user_id,
        jti=jti,
        revoked=False,
        expires_at=expires_at
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

@app.get("/refresh_tokens/")
def get_all_tokens(db: Session = Depends(get_db)):
    tokens = db.query(models.RefreshToken).all()
    return tokens


@app.put("/refresh_tokens/{token_id}/revoke")
def revoke_token(token_id: int, db: Session = Depends(get_db)):
    token = db.query(models.RefreshToken).filter(models.RefreshToken.id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    token.revoked = True
    db.commit()
    db.refresh(token)
    return token

@app.delete("/refresh_tokens/{token_id}")
def delete_token(token_id: int, db: Session = Depends(get_db)):
    token = db.query(models.RefreshToken).filter(models.RefreshToken.id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    db.delete(token)
    db.commit()
    return {"detail": "Token deleted"}