from typing import Optional
from datetime import datetime
from uuid import uuid4
from passlib.context import CryptContext
from app.core.security import get_password_hash, verify_password
from app.models.user import UserCreate, UserInDB
from app.db.neo4j import neo4j_driver

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    query = "MATCH (u:User {email: $email}) RETURN u"
    async with neo4j_driver.driver.session() as session:
        result = await session.run(query, email=email)
        record = await result.single()
        if record:
            node = record["u"]
            return UserInDB(
                id=node["id"],
                email=node["email"],
                hashed_password=node["hashed_password"],
                nickname=node.get("nickname"),
                is_active=node.get("is_active"),
                is_superuser=node.get("is_superuser"),
                profile_image=node.get("profile_image"),
                created_at=node["created_at"].to_native(),
                updated_at=node["updated_at"].to_native(),
            )
    return None

async def create_user(user: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    user_id = str(uuid4())
    now = datetime.now()
    
    query = """
    CREATE (u:User {
        id: $id,
        email: $email,
        hashed_password: $hashed_password,
        nickname: $nickname,
        is_active: $is_active,
        is_superuser: $is_superuser,
        profile_image: $profile_image,
        created_at: $created_at,
        updated_at: $updated_at
    })
    RETURN u
    """
    
    params = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "nickname": user.nickname,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "profile_image": user.profile_image,
        "created_at": now,
        "updated_at": now
    }
    
    async with neo4j_driver.driver.session() as session:
        result = await session.run(query, **params)
        record = await result.single()
        node = record["u"]
        
        return UserInDB(
            id=node["id"],
            email=node["email"],
            hashed_password=node["hashed_password"],
            nickname=node.get("nickname"),
            is_active=node.get("is_active"),
            is_superuser=node.get("is_superuser"),
            profile_image=node.get("profile_image"),
            created_at=node["created_at"].to_native(),
            updated_at=node["updated_at"].to_native(),
        )

async def authenticate(email: str, password: str) -> Optional[UserInDB]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
