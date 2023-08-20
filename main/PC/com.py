#biblioteka do obslugi komunikacji raspoberry pi ze strona przez WebSocket
import asyncio
import websockets

async def handle_connection(websocket, path):
    try:
        while True:
            # Odbieranie wiadomości od klienta
            message = await websocket.recv()
            print(f"otrzymano wiadomosc: {message}")

            # Odpowiedź do klienta
            response = f"otrzymano wiadomosc: {message}"
            await websocket.send(response)
            print(f"wyslano: {response}")

    except websockets.exceptions.ConnectionClosed:
        print("koniec polaczenia")

start_server = websockets.serve(handle_connection, "localhost", 8765)

# Rozpoczęcie pętli głównej
async def main():
    await start_server
    print("polaczono z raspberry ws://localhost:8765")
    await asyncio.Event().wait() 

# Uruchomienie pętli głównej
asyncio.run(main())



#----------------------wysylanie------------------------------
import asyncio
import websockets

async def send_message():
    async with websockets.connect("ws://localhost:8765") as websocket:
        message = "wiadomosc"
        await websocket.send(message)
        print(f"wyslano wiadomosc do raspberry: {message}")

async def main():
    await send_message()

asyncio.run(main())
