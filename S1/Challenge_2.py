s1='1c0111001f010100061a024b53535009181c'
s2='686974207468652062756c6c277320657965'

def xor_hex(s1,s2):
    assert len(s1)== len(s2)
    bs1=bytes.fromhex(s1)
    bs2=bytes.fromhex(s2)
    return bytes([b1^b2 for b1,b2 in zip(bs1,bs2)])

print(xor_hex(s1,s2).hex())