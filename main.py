from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

with open('index.html', 'r') as f:
    html = f.read()


@app.get("/")
async def get():
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8080,
        reload=True
    )