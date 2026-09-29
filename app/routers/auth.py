from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UsuarioModel
from app.schemas import UsuarioLogin, UsuarioRespuesta
from app.security import verify_password, create_access_token
from datetime import timedelta

router = APIRouter(tags=["Autenticación"])

@router.post("/login")
def login_for_access_token(form_data: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.email == form_data.email).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    
    access_token_expires = timedelta(minutes=60*24)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UsuarioRespuesta.from_orm(user)
    }