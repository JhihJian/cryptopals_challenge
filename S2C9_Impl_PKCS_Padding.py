def pkcs7_pad(message, block_size):
    if len(message) == block_size:
        return message
    ch = block_size - len(message) % block_size
    return message + bytes([ch] * ch)

def is_pkcs7_padded(binary_data):
    """Returns whether the data is PKCS 7 padded."""
    # Take what we expect to be the padding
    padding = binary_data[-binary_data[-1]:]
    # Check that all the bytes in the range indicated by the padding are equal to the padding value itself
    return all(padding[b] == len(padding) for b in range(0, len(padding)))

def pkcs7_unpad(data):
    """Unpads the given data from its PKCS 7 padding and returns it."""
    if len(data) == 0:
        raise Exception("The input data must contain at least one byte")
    if not is_pkcs7_padded(data):
        return data

    return data[:-data[-1]]

if __name__ == '__main__':
    assert pkcs7_pad("YELLOW SUBMARINE".encode(),20) == b"YELLOW SUBMARINE\x04\x04\x04\x04"
    print(is_pkcs7_padded(pkcs7_pad("YELLOW SUBMARINE".encode(),20)))
    print(pkcs7_unpad(pkcs7_pad("YELLOW SUBMARINE".encode(),20)))