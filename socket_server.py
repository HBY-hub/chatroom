import socket
import hashlib
import base64

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8008))
sock.listen(10)


def extract_header(data):

    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    header_raw= data.decode()
    print(header_raw)
    header_raw = header_raw.strip()  # 处理可能的空字符
    header_raw = header_raw.split("\n")  # 分割每行
    header_raw = [line.split(":", 1) for line in header_raw]  # 分割冒号
    header_raw.pop(0)
    header_raw = dict((k.strip(), v.strip()) for k, v in header_raw)  # 处理可能的空字符
    print(header_raw)
    return header_raw
    #return dict(line.split(": ", 1) for line in data.split("\n"))


def create_response_header(websocket_headers):
    websocket_key = websocket_headers["Sec-WebSocket-Key"]
    headers = [
        "HTTP/1.1 101 Switching Protocols",
        "Connection: Upgrade",
        "Upgrade: websocket",
        "Sec-WebSocket-Accept:" + base64.b64encode(
            hashlib.sha1((websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
        ).decode(),
        #"WebSocket-Location:" + "ws://%s%s" % (websocket_headers["Host"], websocket_headers["url"])
        "WebSocket-Location:" + "ws://127.0.0.1:8008/chatsocket"
    ]
    return "\r\n".join(headers) + "\r\n\r\n"


def send_msy(conn, msg_bytes):
    import struct
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
    msg = token + msg_bytes
    conn.send(msg)
    return True


def parse_msg(message):
    payload_len = message[1] & 127
    if payload_len == 126:
        extend_payload_len = message[2:4]
        mask = message[4:8]
        decoded = message[8:]
    elif payload_len == 127:
        extend_payload_len = message[2:10]
        mask = message[10:14]
        decoded = message[6:]
    else:
        extend_payload_len = None
        mask = message[2:6]
        decoded = message[6:]

    bytes_list = bytearray()
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    msg = str(bytes_list, encoding='utf-8')
    return msg


while True:
    print("等待连接")
    client, addr = sock.accept()
    print(sock, addr)
    data = client.recv(1024)
    headers = extract_header(data)
    response_header = create_response_header(headers)
    print(response_header)
    client.send(bytes(response_header, "utf-8"))

    while True:
        print("等待数据")

        data = parse_msg(client.recv(1024))
        print(data)
        send_msy(client, bytes(data, encoding="utf-8"))
        if data == "quit###":
            print("close")
            client.close()
            break
