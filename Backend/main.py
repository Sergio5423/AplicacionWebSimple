import uuid
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Contacto
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CAMBIO CRÍTICO AQUÍ ---
try:
    # Intentamos crear las tablas, pero si falla, no detenemos la App
    Base.metadata.create_all(bind=engine)
    print("Conexión a DB exitosa.")
except Exception as e:
    print(f"ERROR: No se pudo conectar a la DB: {e}")
    print("Iniciando modo degradado para responder Health Checks...")
# ---------------------------

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

@app.get("/health")
def health_check():
    # Esta ruta salvará tu Target Group
    return {"status": "ok", "message": "Backend is running"}

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