#Encrypt it, under the key "ICE", using repeating-key XOR.
import base64
ice_bytes=bytes( str.encode('ICE'))
print(ice_bytes)
print("keysize="+str(len(ice_bytes)))
text="""Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal
"""
result_bytes=[]
index=0
for b in str.encode(text):
    result_bytes.append(b^ice_bytes[index])
    index=(index+1)%3
# print((bytes(result_bytes).hex()))
print(base64.encodebytes( (bytes(result_bytes))))