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


@app.get('/{phrase}')
async def get_msg():
    return HTMLResponse(script)


@app.websocket("/ws/{phrase}")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(data.upper())
    await websocket.close()
