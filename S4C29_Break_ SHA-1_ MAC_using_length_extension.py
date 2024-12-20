from S4C28_Impl_SHA1 import sha1
# 攻击目标，在不读取 salt 的情况下，让valid_message_auth返回True
import struct
salt= b'testk'
def get_message_mac(message):

    return sha1(salt + message)

def valid_message_auth(message,mac):
    check_mac=sha1(salt + message)
    if mac==check_mac:
        return True
    return False


if __name__ == '__main__':
    # message = 'message'
    # mac=message
    # assert valid_message_auth(message,mac) ==False
    # attack begin ------------------------
    guess_salt_len=5
    message=b'm'*(55-guess_salt_len)
    mac=get_message_mac(message)
    h0= int.from_bytes(bytes.fromhex(mac[0:8]),'big')
    h1=int.from_bytes(bytes.fromhex(mac[8:16]),'big')
    h2=int.from_bytes(bytes.fromhex(mac[16:24]),'big')
    h3=int.from_bytes(bytes.fromhex(mac[24:32]),'big')
    h4=int.from_bytes(bytes.fromhex(mac[32:40]),'big')
    fake_mac=sha1(b";admin=true",600,h0, h1, h2, h3, h4)
    # 用
    message +=  b'\x80'+struct.pack('>Q', 440)
    assert valid_message_auth(message+b";admin=true",fake_mac)==True