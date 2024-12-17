import socket
import datetime
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


def load_rsa_private_key(pem_file_path, password=None):
    """
    从PEM文件中加载RSA私钥
    :param pem_file_path: PEM文件路径
    :param password: 私钥密码（如果有的话），默认为None
    :return: RSA私钥对象
    """
    with open(pem_file_path, "rb") as key_file:
        private_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return private_key


def send_udp_request(ip, port, verification_code, pem_file_path):
    """
    向指定IP和端口发送UDP请求
    :param ip: 目标IP地址
    :param port: 目标端口号
    :param verification_code: 指定的验证码
    :param pem_file_path: PEM文件路径，包含RSA私钥
    :return: None
    """
    # 获取当前时间戳（秒级）
    timestamp = str(int(datetime.datetime.now().timestamp()))

    # 构造请求体：时间戳 + 验证码
    request_body = timestamp + verification_code

    # 从PEM文件中加载RSA私钥
    private_key = load_rsa_private_key(pem_file_path)

    # 由于cryptography库默认使用OAEP填充，并且不提供关闭OAEP的选项，
    # 我们将使用OAEP并指定一个空的标签（这与C#中的默认行为可能不完全相同，
    # 但OAEP本身是一个安全的填充方案）。
    # 注意：如果你确实需要不使用OAEP的填充，请明确这一点，并意识到这样做可能会降低安全性。
    ciphertext = private_key.encrypt(
        request_body.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None  # 空的标签
        )
    )

    # 将加密后的数据转为Base64编码
    encoded_request_body = base64.b64encode(ciphertext).decode('utf-8')

    # 创建UDP套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 发送UDP请求
        udp_socket.sendto(encoded_request_body.encode(), (ip, port))
        print(f"Sent UDP request to {ip}:{port} with encrypted and base64-encoded body: {encoded_request_body}")
        # 设置一个缓冲区大小来接收响应
        buf_size = 1024
        # 等待并接收响应（注意：这里会阻塞，直到收到数据或发生超时/错误）
        data, server = udp_socket.recvfrom(buf_size)
        print(f'Received {len(data)} bytes from {server}: {data}')
    except Exception as e:
        print(f"Failed to send UDP request: {e}")
    finally:
        # 关闭UDP套接字
        udp_socket.close()


# 示例用法
if __name__ == "__main__":
    target_ip = "106.37.174.61"
    target_port = 27008
    verification_code = "FriG9UKwPTNYTxY"
    pem_file_path = "C:\\0-WorkSpace\\0-工作日报\\环境配置\\k01-client\\public(2)(1).pem"

    send_udp_request(target_ip, target_port, verification_code, pem_file_path)