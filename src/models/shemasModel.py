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
    
class ClaseSchema(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = None
    
class UnidadSchema(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)

class ActividadSchema(BaseModel):
    nombre: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    valor: Optional[float] = None
    fecha_entrega: Optional[date] = None
    fecha_agregada: Optional[time] = None

class EvaluacionSchema(BaseModel):
    calificacion: Optional[float] = None
    autoevaluacion: Optional[float] = None
    entregada: Optional[bool] = None