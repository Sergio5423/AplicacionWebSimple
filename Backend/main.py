import uuid
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Contacto
from pydantic import BaseModel

app = FastAPI()

# Crear tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

# Dependencia para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Contact(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    correo: str

@app.post("/contactos/")
async def create_contact(contacto: Contact, db: Session = Depends(get_db)):
    contact_id = str(uuid.uuid4())[:8]
    nuevo = Contacto(
        id=contact_id,
        nombre=contacto.nombre,
        apellido=contacto.apellido,
        telefono=contacto.telefono,
        correo=contacto.correo
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"message": "Contacto Guardado", "id": nuevo.id}

@app.get("/contactos/")
async def get_contactos(db: Session = Depends(get_db)):
    contactos = db.query(Contacto).all()
    return contactos

@app.delete("/contactos/{contact_id}")
async def delete_contact(contact_id: str, db: Session = Depends(get_db)):
    contacto = db.query(Contacto).filter(Contacto.id == contact_id).first()
    if not contacto:
        return {"error": "Contacto no encontrado"}
    db.delete(contacto)
    db.commit()
    return {"message": "Contacto eliminado correctamente"}