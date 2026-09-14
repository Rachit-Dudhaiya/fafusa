import asyncio
import websockets
import json
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

rooms = {}
client_info = {} 

async def handler(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            
            if action == "CREATE_ROOM":
                code = data["code"]
                player_id = data["playerId"]
                player_name = data["playerName"]
                
                rooms[code] = {
                    "clients": {websocket},
                    "players": [{"id": player_id, "name": player_name, "score": 0}],
                    "host_id": player_id,
                    "answers": {}
                }
                client_info[websocket] = {"room": code, "id": player_id, "name": player_name}
                
                await websocket.send(json.dumps({"type": "ROOM_STATE", "players": rooms[code]["players"]}))
                
            elif action == "JOIN_ROOM":
                code = data["code"]
                player_id = data["playerId"]
                player_name = data["playerName"]
                
                if code in rooms:
                    rooms[code]["clients"].add(websocket)
                    existing = [p for p in rooms[code]["players"] if p["id"] == player_id]
                    if not existing:
                        rooms[code]["players"].append({"id": player_id, "name": player_name, "score": 0})
                        
                    client_info[websocket] = {"room": code, "id": player_id, "name": player_name}
                    
                    msg = json.dumps({"type": "ROOM_STATE", "players": rooms[code]["players"]})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                else:
                    await websocket.send(json.dumps({"type": "ERROR", "message": "Room not found! Ensure the host has created the room first."}))
                    
            elif action == "LEAVE_ROOM":
                await handle_disconnect(websocket)
                
            elif action == "START_ROLL":
                code = client_info.get(websocket, {}).get("room")
                if code in rooms:
                    msg = json.dumps({"type": "START_ROLL"})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
            elif action == "STOP_ROLL":
                code = client_info.get(websocket, {}).get("room")
                letter = data.get("letter")
                if code in rooms:
                    msg = json.dumps({"type": "STOP_ROLL", "letter": letter})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
            elif action == "PLAY_ROUND":
                code = client_info.get(websocket, {}).get("room")
                if code in rooms:
                    rooms[code]["answers"] = {} 
                    msg = json.dumps({"type": "PLAY_ROUND"})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
            elif action == "END_ROUND":
                code = client_info.get(websocket, {}).get("room")
                by_name = data.get("by")
                if code in rooms:
                    msg = json.dumps({"type": "END_ROUND", "by": by_name})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
            elif action == "SUBMIT_ANSWERS":
                code = client_info.get(websocket, {}).get("room")
                p_id = client_info.get(websocket, {}).get("id")
                answers = data.get("answers", {})
                if code in rooms:
                    rooms[code]["answers"][p_id] = answers
                    msg = json.dumps({"type": "SYNC_ANSWERS", "answers": rooms[code]["answers"]})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
            elif action == "TOGGLE_SCORE":
                code = client_info.get(websocket, {}).get("room")
                if code in rooms:
                    msg = json.dumps({
                        "type": "TOGGLE_SCORE", 
                        "roundNum": data.get("roundNum"),
                        "category": data.get("category"),
                        "playerId": data.get("playerId"),
                        "approved": data.get("approved")
                    })
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
            elif action == "PROCEED_NEXT_ROUND":
                code = client_info.get(websocket, {}).get("room")
                if code in rooms:
                    msg = json.dumps({"type": "PROCEED_NEXT_ROUND"})
                    for c in rooms[code]["clients"]:
                        await c.send(msg)
                        
    except websockets.ConnectionClosed:
        pass
    finally:
        await handle_disconnect(websocket)

async def handle_disconnect(websocket):
    info = client_info.get(websocket)
    if info:
        code = info["room"]
        p_id = info["id"]
        if code in rooms:
            if websocket in rooms[code]["clients"]:
                rooms[code]["clients"].remove(websocket)
            
            if rooms[code]["host_id"] == p_id:
                msg = json.dumps({"type": "ROOM_DESTROYED"})
                for c in rooms[code]["clients"]:
                    try:
                        await c.send(msg)
                    except:
                        pass
                del rooms[code]
            else:
                rooms[code]["players"] = [p for p in rooms[code]["players"] if p["id"] != p_id]
                msg = json.dumps({"type": "ROOM_STATE", "players": rooms[code]["players"]})
                for c in list(rooms[code]["clients"]):
                    try:
                        await c.send(msg)
                    except:
                        pass
        del client_info[websocket]

async def main():
    import os
    port = int(os.environ.get("PORT", 8091))
    print(f"Starting WebSocket Server on port {port}...")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

def run_http_server():
    print("Starting HTTP Server on port 8090...")
    server = HTTPServer(("0.0.0.0", 8090), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=run_http_server, daemon=True)
    t.start()
    asyncio.run(main())
