from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid  # Librería para generar IDs únicos

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
    contact_id = str(uuid.uuid4())[:8] 
    with open("contactos/contactos.txt", "a") as f:
        f.write(f"{contact_id},{contacto.nombre},{contacto.apellido},{contacto.telefono},{contacto.correo}\n")
    return contact_id

@app.post("/contactos/")
async def create_contact(contacto: Contact):
    id_generado = save(contacto)
    return {"message": "Contacto Guardado", "id": id_generado}

@app.get("/contactos/")
async def get_contactos():
    contactos_lista = []
    if os.path.exists("contactos/contactos.txt"):
        with open("contactos/contactos.txt", "r") as f:
            for linea in f:
                if linea.strip():
                    partes = linea.strip().split(",")
                    # Ahora el orden es: id, nombre, apellido, tel, correo
                    contactos_lista.append({
                        "id": partes[0],
                        "nombre": partes[1],
                        "apellido": partes[2],
                        "telefono": partes[3],
                        "correo": partes[4]
                    })
    return contactos_lista

@app.delete("/contactos/{contact_id}")
async def delete_contact(contact_id: str):
    if not os.path.exists("contactos/contactos.txt"):
        return {"error": "Archivo no encontrado"}

    with open("contactos/contactos.txt", "r") as f:
        lineas = f.readlines()

    # Filtramos por el ID (índice 0)
    nuevas_lineas = [l for l in lineas if l.strip() and l.strip().split(",")[0] != contact_id]

    with open("contactos/contactos.txt", "w") as f:
        f.writelines(nuevas_lineas)

    return {"message": "Contacto eliminado correctamente"}