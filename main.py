import fastapi
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Crea la base de datos
conn = sqlite3.connect("sql/dispositivos.db")

app = fastapi.FastAPI()

# Origenes para conectarse
origins = [
    "http://0.0.0.0:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://wokwi.com/projects/382859099210315777",
    "https://wokwi.com/projects/382865395767955457",
    "https://frontend-iot-jadc-779b55abc7f3.herokuapp.com"
]

# Opciones de origenes, credenciales, métodos y headers
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Dispositivos(BaseModel):
    id : str
    nombre : str
    valor : str

@app.get("/")
def inicio():
    return {'Developer by':'Jose Dominguez f:', "IoT Proyect": "Primera API IoT"}

# Endpoints para las operaciones
@app.get("/dispositivos")
async def obtener_dispositivos():
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos')
    response = []
    for row in c:
        dispositivo = {"id": row[0], "dispositivo": row[1], "valor":row[2]}
        response.append(dispositivo)
    return response


@app.get("/dispositivos/{id}")
async def obtener_dispositivo(id: str):
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos WHERE id = ?', (id))
    dispositivo = None
    for row in c:
        dispositivo = {"id": row[0],"dispositivo": row[1], "valor": row[2]}
    return dispositivo


@app.put("/dispositivos/{id}")
async def actualizar_dispositivo(id: str, dispositivo: Dispositivos):
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET dispositivo = ?, valor = ? WHERE id = ?',
              (dispositivo.nombre, dispositivo.valor, id))
    conn.commit()
    return dispositivo
