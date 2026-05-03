from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, time

class UsuarioBaseShema(BaseModel):
    nombre: str= Field(min_length=3, max_length=100)
    apellido: Optional[str] = None
    email: EmailStr
    password: str= Field(min_length=8)
    telefono: Optional[str] = None
    fecha: Optional[str] = None
    
class UsuarioShema(UsuarioBaseShema):
    email: EmailStr
    password: str= Field(min_length=8)

class ActividadSchema(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = None
    fecha_limite: Optional[date] = None
    hora_limite: Optional[time] = None
    prioridad: Optional[str] = "media"
    clasificacion: Optional[str] = "personal"