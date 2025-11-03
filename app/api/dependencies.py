from fastapi import Depends, HTTPException, status
from app.models.user_models import User

# Dummy user database
users_db = {
    "alice": User(username="alice", email="alice@example.com", is_admin=True),
    "bob": User(username="bob", email="bob@example.com", is_admin=False),
}

async def get_current_user(username: str = "alice") -> User:
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user
