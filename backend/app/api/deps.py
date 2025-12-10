from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from app.core import security
from app.core.config import settings
from app.models.user import TokenPayload, User
from app.db.neo4j import neo4j_driver

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

async def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Check user in Neo4j
    # This is a placeholder for the actual Neo4j query execution
    # In a real implementation, we would call a service or repository
    query = """
    MATCH (u:User {email: $email})
    RETURN u
    """
    
    if not neo4j_driver.driver:
        await neo4j_driver.verify_connectivity()

    async with neo4j_driver.driver.session() as session:
        result = await session.run(query, email=token_data.sub)
        record = await result.single()
        
        if not record:
             raise HTTPException(status_code=404, detail="User not found")
        
        user_node = record["u"]
        # Convert Neo4j node to User Pydantic model
        # Note: Handling datetime conversion from Neo4j DateTime might be needed
        return User(
            id=user_node.element_id, # or user_node["id"] if we store UUID
            email=user_node["email"],
            nickname=user_node.get("nickname"),
            is_active=user_node.get("is_active", True),
            is_superuser=user_node.get("is_superuser", False),
            profile_image=user_node.get("profile_image"),
            created_at=user_node["created_at"].to_native(),
            updated_at=user_node["updated_at"].to_native(),
        )
