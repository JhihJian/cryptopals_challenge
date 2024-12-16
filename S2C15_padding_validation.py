from S2C9_Impl_PKCS_Padding import is_pkcs7_padded,pkcs7_unpad
assert is_pkcs7_padded(b'ICE ICE BABY\x04\x04\x04\x04')==True
assert pkcs7_unpad(b'ICE ICE BABY\x04\x04\x04\x04')==b'ICE ICE BABY'
assert is_pkcs7_padded(b"ICE ICE BABY\x01\x02\x03\x04")==False
