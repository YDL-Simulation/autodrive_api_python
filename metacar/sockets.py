import cv2
import numpy as np
import socket
import struct
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionClosedError(ConnectionError):
    pass


class SocketBase:
    """
    一个简单的 TCP 服务器基类，实现基于长度 + 内容格式的基本分包。
    长度为 4 字节的无符号整数，使用网络字节序（大端序）。
    仅支持单个客户端连接。
    """

    _HEADER_SIZE = 4  # 消息长度的 4 字节前缀

    def __init__(self, host: str, port: int):
        """
        初始化 socket 服务器。

        :param host: 服务器绑定的 IP 地址。
        :param port: 监听的端口号。
        """
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen()
        self._conn = None
        logger.info(f"监听 {self._host}:{self._port}")

    def accept(self):
        """
        接受一个新的客户端连接。
        如果已有客户端连接，则先关闭旧连接。
        """
        if self._conn:
            self._conn.close()
        self._conn, address = self._sock.accept()
        logger.info(f"{self._host}:{self._port}已连接到{address}")

    def send(self, data: bytes):
        """
        发送数据到客户端，数据前加上 4 字节的长度前缀。

        :param data: 需要发送的字节数据。
        """
        if not self._conn:
            raise ConnectionError("无客户端连接")
        length_prefix = struct.pack("!I", len(data))  # 将长度转换为 4 字节大端序
        self._conn.sendall(length_prefix + data)

    def recv(self) -> bytes:
        """
        从客户端接收数据，确保按照长度前缀读取完整的消息。

        该方法首先读取 4 字节的长度前缀，然后根据前缀指定的长度读取实际消息内容。
        如果连接已关闭，则返回空字节。如果没有客户端连接，则抛出 ConnectionError 异常。

        :return: 接收到的字节数据，如果连接已关闭则返回空字节。
        :raises ConnectionError: 当没有客户端连接时抛出。
        """
        if not self._conn:
            raise ConnectionError("无客户端连接")
        length_data = self._recv_exact(self._HEADER_SIZE)
        if not length_data:
            return b""
        message_length = struct.unpack("!I", length_data)[0]  # 解包 4 字节大端整数
        return self._recv_exact(message_length)

    def _recv_exact(self, size: int) -> bytes:
        """
        精确接收指定字节数的数据。

        :param size: 需要接收的字节数。
        :return: 接收到的字节数据，如果连接已关闭则返回空字节。
        """
        data = bytearray()
        while len(data) < size:
            chunk = self._conn.recv(size - len(data))
            if not chunk:
                return b""  # 连接已关闭
            data.extend(chunk)
        return bytes(data)

    def close(self):
        """
        关闭服务器 socket 及客户端连接。
        """
        if self._conn:
            self._conn.close()
        self._sock.close()
        logger.info(f"{self._host}:{self._port}已关闭")


class JsonSocket(SocketBase):
    """
    支持双向 JSON 通信的 Socket。
    """

    def send(self, data):
        """
        发送 JSON 数据。

        :param data: 需要发送的 JSON 数据。
        """
        return super().send(json.dumps(data).encode())

    def recv(self):
        """
        接收 JSON 数据。

        :return: 接收到的 JSON 数据。
        :raises ConnectionClosedError: 当连接已关闭时抛出。
        """
        raw_data = super().recv()
        if not raw_data:
            raise ConnectionClosedError("连接已关闭")
        return json.loads(raw_data)


class StreamingSocket(SocketBase):
    """
    支持单向接收视频流的 Socket。
    """

    def send(self, data):
        """
        由于是单向接收视频流，禁用 send 方法。

        :raises NotImplementedError: 该方法未实现。
        """
        raise NotImplementedError("send is not supported for StreamingSocket")

    def recv(self):
        """
        接收视频帧。

        :return: 接收到的视频帧。
        :rtype: numpy.ndarray
        :raises ConnectionClosedError: 当连接已关闭时抛出。
        """
        raw_image = super().recv()
        if not raw_image:
            raise ConnectionClosedError("连接已关闭")
        frame = cv2.imdecode(np.frombuffer(raw_image, np.uint8), cv2.IMREAD_COLOR)
        return frame
