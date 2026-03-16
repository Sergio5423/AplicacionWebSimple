from sqlalchemy import Column, String
from database import Base

class Contacto(Base):
    __tablename__ = "contactos"

    id = Column(String(8), primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    telefono = Column(String(20))
    correo = Column(String(100))