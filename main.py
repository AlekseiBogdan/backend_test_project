from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket

app = FastAPI()

script = """
<html>
    <head>
        <title>example</title>
        <style>
            body {
                font-family: sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            div {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
    </head>
    <body>
        <div></div>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws/{phrase}");
            
            const phrase = window.location.href.split('/').slice(-1);
            
            ws.addEventListener("open", (event) => {
                ws.send(phrase);
            });
            
            ws.addEventListener("message", (event) => {
                const resp = document.createElement('h1');
                resp.appendChild(document.createTextNode(event.data));
                document.getElementsByTagName("div")[0].appendChild(resp);
            });
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@app.get('/{phrase}')
async def get_msg():
    return HTMLResponse(script)


@app.websocket("/ws/{phrase}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    data = await websocket.receive_text()
    await manager.send_personal_message(data.upper(), websocket)
    manager.disconnect(websocket)
    await websocket.close()

