
# ==============================
# File: common/protocol.py
# ==============================
import asyncio
import json
import struct
import socket

ENCODING = "utf-8"


def encode_message(obj: dict) -> bytes:
    payload = json.dumps(obj, ensure_ascii=False).encode(ENCODING)
    length = len(payload).to_bytes(4, "big")
    return length + payload


async def decode_message_async(reader: asyncio.StreamReader) -> dict:
    # Leer 4 bytes de longitud
    length_bytes = await reader.readexactly(4)
    length = int.from_bytes(length_bytes, "big")
    data = await reader.readexactly(length)
    return json.loads(data.decode(ENCODING))




def read_exact(sock: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed")
        buf += chunk
    return buf


def decode_message_sync(sock: socket.socket) -> dict:
    length_bytes = read_exact(sock, 4)
    length = struct.unpack(">I", length_bytes)[0]
    data = read_exact(sock, length)
    return json.loads(data.decode(ENCODING))


def send_message_sync(sock: socket.socket, obj: dict) -> None:
    sock.sendall(encode_message(obj))
