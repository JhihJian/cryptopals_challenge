import hashlib


def get_file_md5(file_path):
    # 创建一个hash对象，算法为md5
    md5_hash = hashlib.md5()

    # 打开文件，以二进制模式读取
    with open(file_path, "rb") as f:
        # 分块读取文件，并更新到hash对象中
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    # 获取十六进制格式的hash值
    return md5_hash.hexdigest()


# 示例使用
file_path = "C:\\Users\\98085\\Downloads\\27120bd8-e273-4528-97a9-28dcebe236de\\MD5\\题目.txt"
md5_value = get_file_md5(file_path)
print(f"MD5: {md5_value}")
md5_hash = hashlib.md5()
hashlib.md5().update(b'e00cf25ad42683b3df678c61f42c6bda')
print(f"MD5: { md5_hash.hexdigest()}")
