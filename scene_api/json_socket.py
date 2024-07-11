import socket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionClosedError(Exception):
    pass

class JsonSocket:
    _SEPERATOR = b"|end"

    def __init__(self):
        self._buffer = b""

    # 建立TCP连接
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 5061))
        sock.listen()
        logger.info("等待连接中...")
        self._conn, address = sock.accept()
        logger.info(f"已连接到{address}")

    def recv(self) -> dict:
        while True:
            pos = self._buffer.find(self._SEPERATOR)
            if pos != -1:
                break
            msg = self._conn.recv(4096)
            if not msg:
                logger.warning("连接中断")
                raise ConnectionClosedError("连接中断")
            self._buffer += msg
        message = self._buffer[:pos]
        self._buffer = self._buffer[pos + len(self._SEPERATOR) :]
        return json.loads(message)

    def send(self, msg: dict):
        msg_bytes = json.dumps(msg).encode("utf-8") + self._SEPERATOR
        self._conn.sendall(msg_bytes)

    def close(self):
        self._conn.close()
        logger.info("连接已关闭")
