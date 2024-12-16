import Challenge_3_Single_byte_XOR_cipher
# 初始化一个空列表来存储文件内容
lines = []

# 打开文件并逐行读取
with open('../resources/S3C19_input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 去除每行末尾的换行符并添加到列表中
        lines.append(line.strip())

# 输出结果查看
print(lines)
for line in lines:
    try:
        result=(Challenge_3_Single_byte_XOR_cipher.one_byte_xor_all_result(line))
    except ValueError as e:
        continue
    if len(result)>0:
        print(result)


# 输出：'Now that the party is jumping\n'
