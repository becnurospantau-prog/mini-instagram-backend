from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, auth, schemas
from datetime import datetime, timedelta
from passlib.hash import bcrypt

# =========================
# USERS
# USERS бөліміне қосу
def update_user(db: Session, user_id: int, user_update):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
# =========================

def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = auth.hash_password(password)

    db_user = models.User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# =========================
# POSTS
# =========================
def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_post(db: Session, author_id: int, caption: str):
    db_post = models.Post(
        author_id=author_id,
        caption=caption
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def update_post(db: Session, post_id: int, caption: str):
    db_post = get_post(db, post_id)
    if not db_post:
        return None

    db_post.caption = caption
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        return False

    db.delete(db_post)
    db.commit()
    return True


# =========================
# MEDIA
# =========================

def create_media(db: Session, media):
    db_media = models.Media(
        post_id=media.post_id,
        url=media.url,
        mime_type=media.mime_type,
        width=media.width,
        height=media.height,
        order_idx=media.order_idx
    )

    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media
from sqlalchemy.orm import Session
import models

def get_media(db: Session):
    return db.query(models.Media).all()

def get_media_item(db: Session, media_id: int):
    return db.query(models.Media).filter(models.Media.id == media_id).first()

def update_media(db: Session, media_id: int, media_data: schemas.MediaUpdate):
    media = db.query(models.Media).filter(models.Media.id == media_id).first()
    if not media:
        return None
    for key, value in media_data.dict(exclude_unset=True).items():
        setattr(media, key, value)
    db.commit()
    db.refresh(media)
    return media



def delete_media(db: Session, media_id: int):
    media = db.query(models.Media).filter(models.Media.id == media_id).first()
    if not media:
        return False
    db.delete(media)
    db.commit()
    return True





# =========================
# LIKES (TOGGLE STYLE)
# =========================

# 🔥 Лайк қою / алып тастау (toggle)
def toggle_like(db: Session, user_id: int, post_id: int):

    # 1️⃣ Бар лайкты тексеру
    existing_like = db.query(models.Like).filter(
        and_(
            models.Like.user_id == user_id,
            models.Like.post_id == post_id
        )
    ).first()

    # 2️⃣ Егер лайк бар болса → unlike
    if existing_like:
        db.delete(existing_like)
        db.commit()

        return {
            "status": "unliked",
            "post_id": post_id
        }

    # 3️⃣ Егер жоқ болса → like
    new_like = models.Like(
        user_id=user_id,
        post_id=post_id
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return {
        "status": "liked",
        "post_id": post_id
    }


# ⭐ Посттың лайк санын алу
def get_likes_count(db: Session, post_id: int):
    count = db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).count()

    return {
        "post_id": post_id,
        "likes_count": count
    }

def get_likes(db: Session, post_id: int):
    count = db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).count()
    return {
        "post_id": post_id,
        "likes_count": count
    }

def get_likes(db: Session, post_id: int):
    likes = db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).all()
    return [{"user_id": like.user_id, "post_id": like.post_id} for like in likes]

def remove_like(db: Session, user_id: int, post_id: int):
    like = db.query(models.Like).filter(
        models.Like.user_id == user_id,
        models.Like.post_id == post_id
    ).first()

    if not like:
        return False

    db.delete(like)
    db.commit()
    return True


# ⭐ Белгілі постты лайктаған қолданушылар
def get_post_likes(db: Session, post_id: int):
    likes = db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).all()

    return likes


# ⭐ Белгілі user лайк басқан посттар
def get_user_likes(db: Session, user_id: int):
    likes = db.query(models.Like).filter(
        models.Like.user_id == user_id
    ).all()

    return likes


# =========================
# COMMENTS
# =========================

def create_comment(db: Session, post_id: int, author_id: int, text: str):
    db_comment = models.Comment(
        post_id=post_id,
        author_id=author_id,
        text=text
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, text: str):
    db_comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id
    ).first()

    if not db_comment:
        return None

    db_comment.text = text
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id
    ).first()

    if not db_comment:
        return False

    db.delete(db_comment)
    db.commit()
    return True


# =========================
# FOLLOWS (TOGGLE)
# =========================

# =====================================================
# FOLLOW LOGIC (TOGGLE)
# =====================================================

from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from fastapi import HTTPException
import models

# =====================================================
# FOLLOW / UNFOLLOW ЛОГИКАСЫ
# =====================================================

def toggle_follow(db: Session, follower_id: int, followee_id: int):
    """
    Жазылу және жазылудан шығуды бір батырмамен басқару (Toggle).
    POST /follows/{user_id} үшін қолданылады.
    """
    # 1. Өз-өзіңе жазылуды тексеру
    if follower_id == followee_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    # 2. Жазылғың келген адам базада бар ма?
    target_user = db.query(models.User).filter(models.User.id == followee_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Базадан жазылудың бар-жоғын іздеу
    existing_follow = db.query(models.Follow).filter(
        and_(
            models.Follow.follower_id == follower_id,
            models.Follow.followee_id == followee_id
        )
    ).first()

    if existing_follow:
        # Unfollow бөлімі
        db.delete(existing_follow)
        db.commit()
        return {"detail": "unfollowed"}
    else:
        # Follow бөлімі
        db_follow = models.Follow(
            follower_id=follower_id,
            followee_id=followee_id,
            created_at=datetime.utcnow()
        )
        db.add(db_follow)
        db.commit()
        db.refresh(db_follow)
        return {"detail": "followed"}

def unfollow_user(db: Session, follower_id: int, followee_id: int):
    """
    Нақты жазылудан шығу функциясы.
    DELETE /follows/{user_id} үшін қолданылады.
    """
    follow_record = db.query(models.Follow).filter(
        and_(
            models.Follow.follower_id == follower_id,
            models.Follow.followee_id == followee_id
        )
    ).first()
    
    if not follow_record:
        # HTTPException маршрутадан шығарылады
        return False
        
    db.delete(follow_record)
    db.commit()
    return True

# =====================================================
# АҚПАРАТ АЛУ (GET)
# =====================================================

def get_followers(db: Session, user_id: int):
    """
    Пайдаланушының барлық жазылушыларын (followers) алу.
    """
    return db.query(models.User).join(
        models.Follow, models.User.id == models.Follow.follower_id
    ).filter(models.Follow.followee_id == user_id).all()

def get_following(db: Session, user_id: int):
    """
    Пайдаланушы кімдерге жазылғанын (following) алу.
    """
    return db.query(models.User).join(
        models.Follow, models.User.id == models.Follow.followee_id
    ).filter(models.Follow.follower_id == user_id).all()

# REFRESH TOKENS
# =========================

def create_refresh_token(db: Session, user_id: int, token: str):
    expires_at = datetime.utcnow() + timedelta(days=7)

    db_token = models.RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_refresh_token(db: Session, token: str):
    return db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token
    ).first()