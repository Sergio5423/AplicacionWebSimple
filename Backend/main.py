from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contact(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    correo: str

def save(contacto: Contact):
    os.makedirs("contactos", exist_ok=True)
    with open("contactos/contactos.txt", "a") as f:
        f.write(f"\n{contacto.nombre},{contacto.apellido},{contacto.telefono},{contacto.correo}")
    return "Guardado"

@app.post("/contactos/")
async def create_contact(contacto: Contact):
    save(contacto)
    return {"message": "Contacto Guardado con éxito", "contacto": contacto}


## Agregando la funcionalidad de ver contactos (Joseph A.)

@app.get("/contactos/")
async def get_contactos():
    contactos_lista = []

    if os.path.exists("contactos/contactos.txt"):
        with open("contactos/contactos.txt", "r") as f:
            lineas = f.readlines()

        for linea in lineas:
            if linea.strip():
                nombre, apellido, telefono, correo = linea.strip().split(",")
                contactos_lista.append({
                    "nombre": nombre,
                    "apellido": apellido,
                    "telefono": telefono,
                    "correo": correo
                })

    return contactos_lista
