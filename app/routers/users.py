from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.core.db import create_user, get_user, update_user, delete_user, list_users

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Obtiene los datos del usuario autenticado."""
    return {"username": current_user.username}

@router.post("/")
async def create_new_user(user: dict, current_user: User = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear usuarios")
    user_id = await create_user(user)
    return {"message": "Usuario creado", "user_id": user_id}

@router.get("/")
async def get_all_users(current_user: User = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver la lista de usuarios")
    users = await list_users()
    return users

@router.put("/{username}")
async def modify_user(username: str, updated_data: dict, current_user: User = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar usuarios")
    success = await update_user(username, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario actualizado correctamente"}

@router.delete("/{username}")
async def remove_user(username: str, current_user: User = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar usuarios")
    success = await delete_user(username)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}